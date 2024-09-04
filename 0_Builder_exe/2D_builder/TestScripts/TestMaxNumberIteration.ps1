# 定义可执行文件的路径
$executable = ".\ttcr2d"  # 使用相对路径或完整路径
$configFile = ".\model2d.par"  # 使用相对路径或完整路径

# 先返回到上一级文件夹
Set-Location ..  # 这会将当前目录设置为上一级文件夹

# 初始化一个空的表格（对象数组）
$results = @()

# 循环遍历 max number of iteration 的值从 20 到 100，每次增加 5
for ($iteration = 20; $iteration -le 100; $iteration += 10) {
    # 更新配置文件中的 max number of iteration 参数
    (Get-Content $configFile) -replace '^\d+\s+# max number of iteration', "$iteration             # max number of iteration" | Set-Content $configFile

    # 运行程序并记录运行时间
    Write-Output "Running with max number of iteration = $iteration"
    $start_time = Get-Date

    # 执行命令并捕获输出
    $output = & $executable -v -p $configFile -t -k -s

    # 提取包含“Time to build grid”和“Time to perform raytracing”的那一行
    $gridTimeLine = $output | Select-String -Pattern "Time to build grid:"
    $raytraceTimeLine = $output | Select-String -Pattern "Time to perform raytracing:"

    # 从中提取实际的时间数值
    $gridTime = $gridTimeLine -replace '.*Time to build grid:\s+([0-9.]+).*','$1'
    $gridTime = [double]::Parse($gridTime)
    
    $raytraceTime = $raytraceTimeLine -replace '.*time to perform raytracing:\s+([0-9.]+).*','$1'
    $raytraceTime = [double]::Parse($raytraceTime)

    $totalTime = $gridTime + $raytraceTime
    $singleRayPathTime = $totalTime / 20

    # 将结果保存到表格中
    $results += [PSCustomObject]@{
        Iteration = $iteration
        GridTimeSeconds = $gridTime
        RaytraceTimeSeconds = $raytraceTime
        TotalTimeSeconds = $totalTime
        SingleRayPathTime = $singleRayPathTime
    }

    Write-Output "Time to build grid with max number of iteration = $iteration, $gridTime seconds"
    Write-Output "Time to perform raytracing with max number of iteration = $iteration, $raytraceTime seconds"
    Write-Output "Total time with max number of iteration = $iteration, $totalTime seconds"
    Write-Output "---------------------------------------"
}

# 回到原来的 TestScripts 目录
Set-Location TestScripts 

# 以表格方式弹出窗口显示数据
$results | Out-GridView -Title "Runtime Results"

# 也可以将结果输出到一个 CSV 文件
$results | Export-Csv -Path ".\TestResult\runtime_TestMaxNumberIteration.csv" -NoTypeInformation
