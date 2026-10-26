# Containers

A compact reference for the chapter. Lessons: [VMs vs containers](01-vms-vs-containers.md), [Docker images and Dockerfiles](02-docker-images-and-dockerfiles.md), [Volumes, networks and Compose](03-volumes-networks-and-compose.md), [Registries and Kubernetes basics](04-registries-and-kubernetes-basics.md).

## Key terms

| Term | Meaning |
|---|---|
| Container | A process on the host kernel with isolated files, processes and network |
| Image | Read-only layered package a container starts from |
| Namespace | Kernel feature giving a process its own view of a resource |
| Cgroup | Kernel feature limiting CPU, memory and other resources |
| Layer | One cached, read-only change to the file system, made by one instruction |
| Tag / digest | Movable version name / immutable content hash |
| Volume / bind mount | Docker-managed storage / host folder mapped into a container |
| Registry | Server that stores and serves images |
| Pod / Deployment / Service | Smallest unit in Kubernetes / keeps N pods running / stable address for pods |

## VM or container

| | Virtual machine | Container |
|---|---|---|
| Kernel | Its own | The host's |
| Start time | Seconds to minutes | Under a second, typically |
| Isolation | Hardware-assisted, strong | Kernel features, weaker |

Details: [VMs vs containers](01-vms-vs-containers.md).

## Docker commands

| Command | What it does |
|---|---|
| `docker run --rm -it IMAGE CMD` | Run a command in a new container, delete it on exit |
| `docker run -d --name N -p 8080:80 IMAGE` | Run in the background, publish host port 8080 to container port 80 |
| `docker run -v NAME:/path IMAGE` | Mount a named volume (use `-v "$PWD":/path` for a bind mount) |
| `docker run -m 64m IMAGE` | Limit memory |
| `docker ps` / `docker ps -a` | List running / all containers |
| `docker logs -f N` | Follow a container's output |
| `docker exec -it N sh` | Open a shell in a running container |
| `docker stop N` / `docker rm N` | Stop / remove a container |
| `docker build -t name:tag .` | Build an image from the Dockerfile in this folder |
| `docker build --platform linux/amd64 .` | Build for a specific architecture |
| `docker images` / `docker rmi IMAGE` | List / remove images |
| `docker tag SRC DEST` | Add a name to an image |
| `docker push` / `docker pull` | Upload / download an image |
| `docker volume ls` | List volumes |
| `docker system prune` | Remove stopped containers, unused networks and dangling images (asks first) |

## Dockerfile instructions

| Instruction | What it does |
|---|---|
| `FROM image AS name` | Base image, starts a stage |
| `WORKDIR dir` | Working directory |
| `COPY src dest` / `COPY --from=stage src dest` | Copy from the build context / from another stage |
| `RUN cmd` | Run at build time, saved as a layer |
| `ENV K=v` | Environment variable |
| `EXPOSE port` | Documents a port, does not publish it |
| `USER name` | Run as this user (not root) |
| `ENTRYPOINT ["prog"]` | Fixed program |
| `CMD ["arg"]` | Default command or arguments (exec form) |

Order rarely-changing instructions first. Use a `.dockerignore`. Details: [Docker images and Dockerfiles](02-docker-images-and-dockerfiles.md).

## Compose commands

| Command | What it does |
|---|---|
| `docker compose up -d --build` | Build and start all services |
| `docker compose ps` | Service status |
| `docker compose logs -f SERVICE` | Follow logs |
| `docker compose exec SERVICE CMD` | Run a command in a service |
| `docker compose down` | Remove containers and network, keep volumes |
| `docker compose down -v` | Also delete volumes |

Rules: services reach each other by service name, not `localhost`. Publish only the ports the host needs. Add a healthcheck and `depends_on` with `condition: service_healthy`. The Postgres 18 data path is `/var/lib/postgresql`. Details: [Volumes, networks and Compose](03-volumes-networks-and-compose.md).

## Registries and Kubernetes

| Command | What it does |
|---|---|
| `docker login [registry]` | Authenticate |
| `docker tag app:1 ghcr.io/USER/app:1.4.2` | Name for pushing |
| `kubectl apply -f file.yaml` | Create or update objects |
| `kubectl get pods` | List pods |
| `kubectl describe pod NAME` | Details and events |
| `kubectl logs NAME` | Pod output |
| `kubectl rollout status deployment/NAME` | Wait for a rollout |

Rules: tag every build uniquely and do not deploy `latest`. A Secret is encoded, not encrypted. Skip Kubernetes when one server with Compose is enough. Details: [Registries and Kubernetes basics](04-registries-and-kubernetes-basics.md).
