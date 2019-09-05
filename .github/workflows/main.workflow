action "login" {
    uses = "actions/docker/login@master"
    secrets = ["REGISTRY_USERNAME", "REGISTRY_PASSWORD"]
}

action "build" {
    uses = "actions/docker/cli-multi@master"
    args = [
        "build -t matootie/kiki:latest .",
        "push matootie/kiki:latest"
    ]
}