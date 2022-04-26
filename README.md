寶寶命名機器人
==

## 組員
- 經濟四 余函庭
- 統計四 陳柔漪

## Project 描述
- **主題**  
寶寶命名機器人 

- **內容**  
我們預計設計一個 Chatbot，讓爸媽輸入對於孩子的期許以作為分析文本，再結合筆畫、宗教等等資訊，讓機器人去運算出一個或多個建議的名字，並簡單解釋這些字的涵義。

- **動機**  
人類在取名的時候通常都會賦予名字一些特別的含意，比如說女生的名字常常出現草字頭或水字邊，期許這個女生未來能具備溫柔的特質等等。這些對於特質的想像應該和這個字的語意成分是有所連結的。

- **對話設置**  
透過按鈕來限制使用者的輸入，讓 NLP 能集中在最後一題「講述一下對小孩的期望/希望的特質吧!」
    - line bot 程式用途參考: [SDK of the LINE Messaging API for Python | Github](https://github.com/line/line-bot-sdk-python)
    - 前期遇到的問題: 
        1. PostbackEvent 與 MessageEvent 相撞，前者似乎被後者回應吃掉直接沒反應
        2. ButtonsTemplate 僅能裝下至多4個選項 → 改成使用 CarouselTemplate (故障都不會回報哪裡有問題，這 bug 我找好久QQ)
        3. SQL語法不熟悉，想要設置清除"沒有回答完全"的資料，試了一陣子


- **資料庫設置**  
最後我們決定將所有資料使用 json 檔儲存，置於 dataset 資料夾內。  
希望在相對熟悉的環境下，可以花更多心力在 Chatbot 上面。  


- **模型設置**  
對話互動的資料會存在 User_input.json，並將期許文字分析的模型寫於 models.py，方便。
  - 文本處理流程: text → 以所有標點符號"斷句" → 斷詞 → 詞性標註 
  - 主要抓取詞性標註 VH 作為期望的主要意義
  - 將各斷句進行正負面判斷，正面關鍵詞直接保留，負面則於前方加上「不」，收集於期望的過濾詞清單 (demand_words)
  - 將過濾詞與資料庫中的詞義進行相似度分析，取得門檻值 0.8 以上的所有相似詞作為字清單
  - 篩選使用者輸入的條件 (缺少五行、指定加入的字、同音字)
  - 接著，字清單會進行排列組合，透過名字筆畫算出的五格計算分數，最後排序出 10 個推薦姓名給予使用者

- **回饋面板**  
在機器人回覆特定功能的面板上我們選擇使用 FlexMessage，加入按鈕設置，讓使用者可以簡單進行想要的操作。  
  - 透過以下參考刻出面板 QAQ
  - [FlexMessage Simulator](https://developers.line.biz/flex-simulator/)
  - [linebot.models.flex_message module](https://line-bot-sdk-python.readthedocs.io/en/stable/linebot.models.html#module-linebot.models.flex_message)

- **Demo Video**  
詳細操作置於影片中，歡迎收看 ଘ(੭*ˊᵕˋ)੭  
[【AI Chatbot】Group 1 命名小精靈。夢咕嚕](https://www.youtube.com/watch?v=ukp0lKERbEU)

- **演示圖**  
![](https://github.com/Rou-Yi/GiveName_Linebot/blob/main/LINEBOT%E6%BC%94%E7%A4%BA%E5%9C%96%E7%89%87.jpg?raw=true)
