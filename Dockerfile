FROM debian:buster AS builder

RUN apt-get update && \
    apt-get install -y cmake g++ && \
    rm -rf /var/lib/apt/lists/*


# Build libtglang.so
FROM builder as build-lib

COPY src /src
WORKDIR /src/build

RUN cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build .


# Export libtglang.so
FROM scratch as export-lib
COPY --from=build-lib /src/build/libtglang.so .


# Build tglang-tester
FROM builder AS build-tester

COPY --from=build-lib /src/build/libtglang.so /test/libtglang.so

COPY test /test
WORKDIR /test/build

RUN cmake -DCMAKE_BUILD_TYPE=Release .. && \
    cmake --build .


# Evaluate metrics on test data
FROM debian:buster AS test

RUN apt-get update && \
    apt-get install -y python3 python3-sklearn && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build-lib /src/build/libtglang.so /test/libtglang.so
COPY --from=build-tester /test/build/tglang-tester /test/tglang-tester

COPY test/test.py /test/test.py
ADD test/test.tar.gz /test/

WORKDIR /test

ENTRYPOINT ["python3", "test.py", "/test/tglang-tester", "/test/test.csv"]
