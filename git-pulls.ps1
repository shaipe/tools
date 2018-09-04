# 清除当前窗口输出内容
cls;
# 获取系统脚本当前处理的目录 
$cdir = Split-Path -Parent $MyInvocation.MyCommand.Definition;
Write-Host("当前正在运行的脚本的目录为:$cdir");

# 获取当前目录下的所有子对外象
Get-ChildItem  | ForEach-Object -Process{

    #判断当前对象是否为目录
    if($_ -is [System.IO.DirectoryInfo])
    {
        Write-Host("-----------------对 $cdir/$_ 目录进行处理------------------");
        cd "$cdir/$_";
        $cbranch = "";
        git pull;
        git branch | ForEach-Object -Process{

            if($_.contains("*")){
                # Write-Host($_);
                $cbranch = "git checkout $_".Replace("*","");
            }
            $gb = "git checkout $_".Replace("*","");
            Write-Host("正在对分支 $_ 进行处理".Replace("*",""));
            $executioncontext.InvokeCommand.InvokeScript($gb);
            git pull;
        }
        Write-Host("=====还原git最初分支 $cbranch====");
        if([String]::IsNullOrEmpty($cbranch)){
           
        }
        else{
             $executioncontext.InvokeCommand.InvokeScript($cbranch);
        }
    }
}

Write-Host("处理完毕还原初始目录 === $cdir===");
cd $cdir;
