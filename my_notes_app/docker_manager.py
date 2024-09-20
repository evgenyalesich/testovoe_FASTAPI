import subprocess

# Функция для запуска PostgreSQL контейнера
def run_postgres_container():
    command = [
        "docker", "run", "--name", "testovoe-postgres",
        "-e", "POSTGRES_USER=Evgeny",
        "-e", "POSTGRES_PASSWORD=Myfassa99@",
        "-e", "POSTGRES_DB=testovoe",
        "-p", "5432:5432",
        "-d", "postgres"
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("PostgreSQL контейнер успешно запущен!")
    else:
        print(f"Произошла ошибка при запуске контейнера: {result.stderr}")

# Функция для остановки и удаления контейнера
def stop_postgres_container():
    stop_command = ["docker", "stop", "testovoe-postgres"]
    remove_command = ["docker", "rm", "testovoe-postgres"]

    stop_result = subprocess.run(stop_command, capture_output=True, text=True)
    if stop_result.returncode == 0:
        print("PostgreSQL контейнер успешно остановлен!")
    else:
        print(f"Ошибка при остановке контейнера: {stop_result.stderr}")

    remove_result = subprocess.run(remove_command, capture_output=True, text=True)
    if remove_result.returncode == 0:
        print("PostgreSQL контейнер успешно удален!")
    else:
        print(f"Ошибка при удалении контейнера: {remove_result.stderr}")

if __name__ == "__main__":
    run_postgres_container()  # Запуск контейнера при вызове

