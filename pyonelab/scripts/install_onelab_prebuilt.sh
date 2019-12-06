#!/bin/bash

OS=$1
ONELAB_PATH=$2
VERSION="$3"

if [ $VERSION == "stable" ]; then
  export GMSH_VERSION="4.4.1"
  export GETDP_VERSION="3.2.0"
elif [ $VERSION == "dev" ]; then
  export GMSH_VERSION="git"
  export GETDP_VERSION="git"
else
  exit
fi
#
rm -rf $ONELAB_PATH
mkdir -p $ONELAB_PATH
cd $ONELAB_PATH

echo "  >>> Installing onelab $VERSION for $OS in $ONELAB_PATH"


case $OS in
     Linux)
          EXTRACT="tar -xf "
          ARCHEXT="tgz"
          export GMSH_NAME=gmsh-$GMSH_VERSION-Linux64
          export GMSH_ARCH=Linux/$GMSH_NAME.$ARCHEXT
          export GETDP_NAME=getdp-$GETDP_VERSION-Linux64
          export GETDP_ARCH=Linux/$GETDP_NAME\c.$ARCHEXT

          ;;
     Darwin)
          EXTRACT="tar -xf "
          ARCHEXT="tgz"
          export GMSH_NAME=gmsh-$GMSH_VERSION-MacOSX-sdk
          export GMSH_ARCH=MacOSX/$GMSH_NAME.$ARCHEXT
          export GETDP_NAME=getdp-$GETDP_VERSION-MacOSX
          export GETDP_ARCH=MacOSX/$GETDP_NAME\c.$ARCHEXT
          ;;
     Windows)
         EXTRACT="unzip "
         ARCHEXT="zip"
         export GMSH_NAME=gmsh-$GMSH_VERSION-Windows64
         export GMSH_ARCH=Windows/$GMSH_NAME.$ARCHEXT
         export GETDP_NAME=getdp-$GETDP_VERSION-Windows64
         export GETDP_ARCH=Windows/$GETDP_NAME\c.$ARCHEXT
          ;;
esac


# gmsh

echo "  >>> Installing gmsh..."
wget -cq http://gmsh.info/bin/$GMSH_ARCH -O gmsh.$ARCHEXT
$EXTRACT gmsh.$ARCHEXT
rm gmsh.$ARCHEXT
mv $GMSH_NAME gmsh_tmp
if [ "$OS" == "windows" ]; then
  mv gmsh_tmp/gmsh.exe $ONELAB_PATH
else
  mv gmsh_tmp/bin/gmsh $ONELAB_PATH
fi
if [ "$OS" == "osx" ]; then
  mv gmsh_tmp/lib/*.dylib $ONELAB_PATH
fi
rm -rf gmsh_tmp


# getdp

echo "  >>> Installing getdp..."

wget -cq http://getdp.info/bin/$GETDP_ARCH -O getdp.$ARCHEXT
$EXTRACT getdp.$ARCHEXT
rm getdp.$ARCHEXT
mv $GETDP_NAME getdp_tmp
if [ "$OS" == "windows" ]; then
  mv getdp_tmp/getdp.exe $ONELAB_PATH
else
  mv getdp_tmp/bin/getdp $ONELAB_PATH
fi
rm -rf getdp_tmp


echo "  >>> Installation done."
