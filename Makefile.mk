.PHONY: deb deb-build-env deb-enter-docker

    deb-build-env:
        docker build \
            --file=./debian/Dockerfile \
            --tag=python-deb-pkg \
            ./

    deb: deb-build-env
        if [ ! -d ./debian/dist ]; then \
            mkdir ./debian/dist; \
        fi;
        if [ -e ./debian/dist/*.deb ]; then \
            sudo rm ./debian/dist/*.deb; \
        fi;
        docker run \
            --volume=$$(pwd)/debian/dist:/tmp/python-deb-pkg/debian/dist \
            python-deb-pkg dpkg-buildpackage -us -uc -b --changes-option=-udebian/dist/

    deb-enter-docker:
        docker run \
            --interactive \
            --tty=true \
            --volume=$$(pwd):/tmp/python-deb-pkg \
            python-deb-pkg /bin/bash