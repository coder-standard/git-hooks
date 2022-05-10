#!/bin/bash

SOURCE="$0"
while [ -h "$SOURCE"  ]; do # resolve $SOURCE until the file is no longer a symlink
    DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /*  ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE"  )" && pwd  )"

install_path=/usr/bin
if [[ $# -eq 1 ]]; then
  install_path=$1
fi


cat > $install_path/install-git-hooks.sh <<-EOF
#!/bin/bash
python3 $DIR/install-git-hooks.py \$@
EOF

chmod +x $install_path/install-git-hooks.sh
