from docker import DockerClient
from docker.errors import DockerException, NotFound, ImageNotFound, APIError
import subprocess
import logging


class InitOllama:
    """
        - on_docker (bool): If True, manages Ollama through Docker. If False, runs locally.
    """

    def __init__(self, on_docker: bool = True):
        self.on_docker = on_docker
        self.container_name = "ollama"
        self.image_name = "ollama/ollama"
        self.logger = logging.getLogger(__name__)

        if on_docker:
            try:
                self.client = DockerClient.from_env()
                self._setup_docker_instance()
            except DockerException as e:
                self.logger.error(f"Failed to initialize Docker client: {e}")
                raise
        else:
            self._run_local_instance()

    def _setup_docker_instance(self) -> None:
        try:
            try:
                container = self.client.containers.get(self.container_name)
                if container.status != "running":
                    self.logger.info("Starting existing container")
                    container.start()
                return
            except NotFound:
                pass

            try:
                self.client.images.get(self.image_name)
            except ImageNotFound:
                self.logger.info("Pulling Ollama image")
                self.client.images.pull(self.image_name)

            self.logger.info("Creating and starting new Ollama container")
            self.client.containers.run(
                self.image_name,
                name=self.container_name,
                detach=True,
                ports={'11434/tcp': 11434},
                volumes={'/root/.ollama': {'bind': '/root/.ollama', 'mode': 'rw'}}
            )

        except APIError as e:
            self.logger.error(f"Docker API error: {e}")
            raise

    def _run_local_instance(self) -> None:
        try:
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.logger.info("Started local Ollama instance")
        except FileNotFoundError:
            self.logger.error("Ollama not found in system path")
            raise
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to start Ollama: {e}")
            raise

    def stop(self) -> None:
        if self.on_docker:
            try:
                container = self.client.containers.get(self.container_name)
                container.stop()
                self.logger.info("Stopped Docker container")
            except NotFound:
                self.logger.warning("Container not found")
            except APIError as e:
                self.logger.error(f"Failed to stop container: {e}")
                raise
        else:
            try:
                subprocess.run(
                    ["pkill", "ollama"],
                    check=True,
                    capture_output=True
                )
                self.logger.info("Stopped local Ollama instance")
            except subprocess.SubprocessError as e:
                self.logger.error(f"Failed to stop local instance: {e}")
                raise

    def is_running(self) -> bool:
        if self.on_docker:
            try:
                container = self.client.containers.get(self.container_name)
                return container.status == "running"
            except NotFound:
                return False
        else:
            try:
                output = subprocess.run(
                    ["pgrep", "ollama"],
                    capture_output=True,
                    check=False
                )
                return output.returncode == 0
            except subprocess.SubprocessError:
                return False


