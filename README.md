# 天気から服装提案アプリ
このアプリはその日の天気から服装を提案します。
他の人がその日どんな服を着ているかを確認いただけます。

## URL
https://weather-clothes-app.an.r.appspot.com/clothes

## 使用技術
- Python
- HTML
- CSS
- Django
- MySQL
- Google App Engine
- 天気予報API

<img width="943" alt="スクリーンショット 2022-12-17 15 04 42" src="https://user-images.githubusercontent.com/111218880/208227998-c3a67cb7-96e6-42a2-b8f7-8d6b9c576c70.png">

## 機能紹介1:  簡単に気温と最適な服装を知る事ができる
- 現在地を選択すると気温情報と適切な服装を提示します
- 気温情報取得には、天気予報のAPIを使用
- 現在地を選択できるため、外出先の情報も取得できます

### 参考: 服装の提案パターン
<img width="709" alt="スクリーンショット 2022-12-17 15 14 41" src="https://user-images.githubusercontent.com/111218880/208228247-96e6210c-fbd7-4ddd-84fb-0c108d36a28c.png">

## 機能紹介2:  他のユーザーの服をチェックできる
- ログインをする事で他のユーザーの服装の画像の取得、自身の服装の投稿ができます
- 投稿時には、気温・ユーザーの年齢・画像をセットでデータベースに保存されます
- データベースに保存された画像を気温やユーザー情報をもとに服装を提案します

### 参考: 投稿時のデータの保存の構成図
<img width="829" alt="スクリーンショット 2022-12-17 15 18 31" src="https://user-images.githubusercontent.com/111218880/208228424-94ef6614-52f5-41c7-b91b-a8bf55461e54.png">


