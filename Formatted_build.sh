pyinstaller pyinstaller.spec

platform='unknown'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   platform='linux'
elif [[ "$unamestr" == 'Darwin' ]]; then
   platform='darwin'
elif [[ "$unamestr" == 'Win32' ]]; then
   platform='win32'
fi

if [[ $platform == 'linux' ]]; then
   chmod +x build.sh
   ./build.sh

elif [[ $platform == 'darwin' ]]; then
   chmod +x build_mac
   ./build_mac

elif [[ $platform == 'win32' ]]; then
   chmod +x build_win
   ./build_win
fi
