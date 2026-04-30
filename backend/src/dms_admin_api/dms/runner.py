import http.client
import json
import socket
import subprocess
from collections.abc import Sequence

from dms_admin_api.dms.models import CommandResult


class UnixSocketHTTPConnection(http.client.HTTPConnection):
    def __init__(self, socket_path: str) -> None:
        super().__init__("localhost")
        self.socket_path = socket_path

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)


class CommandRunner:
    def _demux_exec_stream(self, payload: bytes) -> tuple[str, str]:
        stdout = bytearray()
        stderr = bytearray()
        cursor = 0

        while cursor + 8 <= len(payload):
            stream_type = payload[cursor]
            size = int.from_bytes(payload[cursor + 4 : cursor + 8], byteorder="big")
            start = cursor + 8
            end = start + size
            chunk = payload[start:end]

            if stream_type == 1:
                stdout.extend(chunk)
            elif stream_type == 2:
                stderr.extend(chunk)

            cursor = end

        if cursor == 0:
            return payload.decode(), ""

        return stdout.decode(), stderr.decode()

    def _request_json(
        self,
        connection: UnixSocketHTTPConnection,
        method: str,
        path: str,
        body: dict[str, object] | None = None,
    ) -> tuple[int, dict[str, object], bytes]:
        payload = None if body is None else json.dumps(body).encode()
        headers = {"Content-Type": "application/json"} if payload is not None else {}
        connection.request(method, path, body=payload, headers=headers)
        response = connection.getresponse()
        raw = response.read()
        parsed = json.loads(raw.decode()) if raw else {}
        return response.status, parsed, raw

    def _docker_exec_via_socket(self, args: Sequence[str]) -> CommandResult:
        container = args[2]
        command = list(args[3:])
        connection = UnixSocketHTTPConnection("/var/run/docker.sock")

        try:
            status, create_response, _ = self._request_json(
                connection,
                "POST",
                f"/v1.43/containers/{container}/exec",
                {
                    "AttachStdout": True,
                    "AttachStderr": True,
                    "Cmd": command,
                    "Tty": False,
                },
            )
            exec_id = create_response.get("Id")
            if status >= 400 or not isinstance(exec_id, str):
                message = create_response.get("message", "Failed to create Docker exec")
                return CommandResult(stdout="", stderr=str(message), exit_code=1)

            connection.request(
                "POST",
                f"/v1.43/exec/{exec_id}/start",
                body=json.dumps({"Detach": False, "Tty": False}).encode(),
                headers={"Content-Type": "application/json"},
            )
            start_response = connection.getresponse()
            raw_stream = start_response.read()
            stdout, stderr = self._demux_exec_stream(raw_stream)

            _, inspect_response, _ = self._request_json(connection, "GET", f"/v1.43/exec/{exec_id}/json")
            exit_code = inspect_response.get("ExitCode")
            return CommandResult(
                stdout=stdout,
                stderr=stderr,
                exit_code=int(exit_code) if isinstance(exit_code, int) else 1,
            )
        finally:
            connection.close()

    def run(self, args: Sequence[str]) -> CommandResult:
        try:
            completed = subprocess.run(args, capture_output=True, text=True, check=False)
            return CommandResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
            )
        except OSError as error:
            if len(args) >= 4 and args[0] == "docker" and args[1] == "exec":
                try:
                    return self._docker_exec_via_socket(args)
                except OSError as socket_error:
                    return CommandResult(stdout="", stderr=str(socket_error), exit_code=127)
            return CommandResult(stdout="", stderr=str(error), exit_code=127)
