import yaml

def get_user_input(prompt, default=None):
    value = input(f"{prompt} {f'[{default}]' if default else ''}: ").strip()
    return value if value else default

def generate_kubernetes_deployment():
    print("Welcome to the Kubernetes Deployment YAML Generator!")
    print("Please provide the following information:")

    # Collect user inputs
    app_name = get_user_input("Enter the application name")
    image = get_user_input("Enter the container image")
    replicas = int(get_user_input("Enter the number of replicas", "1"))
    container_port = int(get_user_input("Enter the container port", "80"))

    # Create the deployment structure
    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": app_name
        },
        "spec": {
            "replicas": replicas,
            "selector": {
                "matchLabels": {
                    "app": app_name
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app": app_name
                    }
                },
                "spec": {
                    "containers": [
                        {
                            "name": app_name,
                            "image": image,
                            "ports": [
                                {
                                    "containerPort": container_port
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }

    # Convert the deployment to YAML
    yaml_output = yaml.dump(deployment, default_flow_style=False)

    print("\nGenerated Kubernetes Deployment YAML:")
    print("-------------------------------------")
    print(yaml_output)

    # Optionally save to a file
    save_option = get_user_input("Do you want to save this YAML to a file? (y/n)", "n")
    if save_option.lower() == 'y':
        filename = get_user_input("Enter the filename to save", f"{app_name}-deployment.yaml")
        with open(filename, 'w') as file:
            file.write(yaml_output)
        print(f"YAML saved to {filename}")

if __name__ == "__main__":
    generate_kubernetes_deployment()
