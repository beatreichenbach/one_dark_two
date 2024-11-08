# Contributing

## Python

Create a virtual environment for python and install the dependencies:
```shell
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r generate/requirements.txt
```

Generate the variants:
```shell
./venv/bin/python3 generate/generate.py
```

## Gradle

Add gradlew:
```shell
gradle wrapper --gradle-version 8.10.2 --distribution-type bin
```

Build the plugin:
```shell
./gradlew build
```

Re-generate the variants and run the plugin in an IDE:
```shell
./venv/bin/python3 generate/generate.py && ./gradlew runIde
```

Clean re-build
```shell
rm -rf build && ./venv/bin/python3 generate/generate.py && ./gradlew build
```
