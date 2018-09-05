#!/bin/bash

work_path=$(pwd)   # 取到脚本目录 

echo '当前正在运行脚本的目录为:' ${work_path}

# 下面的方法可以获取到当前脚本运行目录
# echo '$0: '$0
# echo "pwd: "`pwd`
# echo "============================="
# echo "scriptPath1: "$(cd `dirname $0`; pwd)
# echo "scriptPath2: "$(pwd)

# 遍历当前目录下的所有文件或目录
function read_dir () {  
    # $1 表示传入的第一个参数
    for file in ` ls $1 `  
    do  
        # 判断是否为目录
        if [ -d $1"/"$file ]   
        then  
            echo $1"/"$file
            git_pull $1"/"$file
            # ergodic $1"/"$file  
        else  # 文件
            echo "$1/$file" 
        fi  
    done  
} 

# git 目录获取
function git_pull(){
    echo "正在"$1"目录进行git操作"
    bs=$(gset -f; git branch)
    # echo DD
    for b in $bs
    do
        echo 'branch:'$b
    done
    echo $bs
}
# for remote in `git branch -r `; do echo 'ee:'$remote; done
for b in `git branch -r | grep -v -- '->'`; do echo $b; done
function git_branch()
{
    branch=''
    cd $PWD
    if [ -d '.git' ]; then
        output=`git describe --contains --all HEAD|tr -s '\n'`
        if [ "$output" ]; then
            branch="(${output})"
        fi
    fi
    echo $branch
}
git_branch

# echo ${branch}
#  git_branch ${work_path}

# cd ~/${work_path}

# SHELL_FOLDER=$(dirname "$0")

# echo SHELL_FOLDER