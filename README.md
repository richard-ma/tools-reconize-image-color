# tools-reconize-image-color

# 安装
* 解压压缩包即可使用

# 使用方法
* 准备好csv文件
* 在csv文件同目录下新建images目录，并把所有待识别的图片都放到这个目录中
* 双击exe文件运行程序
* 拖动csv文件到程序运行窗口，回车确认
* 程序运行
* 结果文件为new_开头后接csv文件名的新文件
    * 识别出的颜色在color列
    * 无法识别的颜色color列为None加上颜色代码
    * 没有找到的图片color列为空，nofound列为no found