# GUI说明
本项目基于B站YY鼠鼠的[使用Kata为日语EPUB文件中的汉字注音（注假名）](https://www.bilibili.com/read/cv28891933/?spm_id_from=333.999.0.0)，用Tkinter添加了一个方便操作的GUI，并且修复了一些导致无法使用的bug。
<br>
</br>
对原版修复的BUG与修改：
<ul>
<li>电子书在转换后排版样式不正确，如日文竖版变回横板</li>
<li>部分电子书识别不到文本导致转换后没有区别</li>
<li>改进临时文件的处理方式，使其兼容MacOS</li>
<li>不会留下运行过程中创建的临时文件</li>
</ul>
目前尚且存在的问题：
<ul>
  <li>已有振假名注音的文字在转换后会有两层振假名注音</li>
</ul>

转换效果
![转换效果](/result.png)

# 以下是原项目的README
<br>
</br>
这是一个用于为日语epub文件中的汉字注音的项目。<br><br>
新版本发表！Kata 2.1 版本引入了多进程计算，大幅提高了运行速度，避免了一核有难多核围观的惨剧。其中，kata_multi_proce_limit.py 可以手动限制进程数量，以防止你的PC成为喷气机。


<br>
</br>
This is a project for adding phonetic annotations to Kanji in Japanese EPUB files.  Please **ensure** to run **setup.exe** before use to prepare the environment.<br><br>
New release! Kata version 2.1 introduces multiprocessing, significantly improving runtime speed and avoiding the tragic scenario of one core struggling while others stand by. In particular, kata_multi_proce_limit.py allows manual limitation of the number of processes to prevent your PC from turning into a jet engine.
<br>
</br>
これは日本語のEPUBファイル内の漢字に注音をつけるプロジェクトです。使用前に、**必ず**環境をセットアップするために**setup.exe**を実行してください。<br><br>
新しいバージョンが発表されました！ Kata 2.1 バージョンでは、マルチプロセス計算が導入され、実行速度が大幅に向上し、1つのコアでの苦労を避けることができます。その中で、kata_multi_proce_limit.py では手動でプロセスの数を制限し、PCがジェットエンジンになるのを防ぐことができます。
<br>
</br>

**效果示例：**

<div align="center">
  <p>处理前</p>
</div>

![处理前](/example.png)

<div align="center">
  <p>处理后</p>
</div>

![处理后](/example.jpg)
<br>
<br>
<br>
<br>

如果这个项目能帮到您,请在能力范围内支持该项目,感谢您的支持！<br>
<br>

If this project has been beneficial to you, kindly consider offering support within your means. We appreciate your backing!<br>
<br>
