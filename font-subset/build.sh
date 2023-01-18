#!/bin/bash

OTF_FILE=OTF/SimplifiedChineseHW/SourceHanSansHWSC-Regular.otf
TTF_FILE=SourceHanSans.ttf
OUTPUT_FILE=SourceHanSansMini.ttf
# TEXT_FILE=8k.txt
TEXT_FILE=hf.txt

SHELL_DIR=$(cd "$(dirname "$0")";pwd)
cd ${SHELL_DIR}

echo "download font..."
if [[ ! -e ${OTF_FILE} ]]; then
    wget https://github.com/adobe-fonts/source-han-sans/releases/download/2.004R/SourceHanSansHWSC.zip
    unzip SourceHanSansHWSC.zip
else
    echo "${OTF_FILE} exists, skip!"
fi

echo "otf2tff..."
if [[ ! -e ${TTF_FILE} ]]; then
    pipenv run otf2ttf -o ${TTF_FILE} ${OTF_FILE}
    echo "${TTF_FILE} ready"
else
    echo "${TTF_FILE} exists, skip!"
fi

echo "subset font..."
pipenv run pyftsubset ${TTF_FILE} --text=`cat ${TEXT_FILE}` --output-file=${OUTPUT_FILE} --no-hinting
echo "output: ${OUTPUT_FILE}"
