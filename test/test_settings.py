from config.settings import Settings


print(Settings.PROJECT_NAME)

print(Settings.VERSION)

print(Settings.CAMERA_SOURCE)

Settings.create_directories()

print("Configuration loaded successfully")