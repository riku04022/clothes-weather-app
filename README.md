# 天気から服装提案アプリ
このアプリはその日の天気から服装を提案します。
他の人がその日どんな服を着ているかを確認いただけます。

## URL
https://clothes-weather-app-374216.an.r.appspot.com

## 使用技術
- Python
- HTML
- CSS
- JavaScript
- Django
- MySQL
- Google App Engine
- 天気予報API (OpenWeatherMap)

<img width="709" alt="スクリーンショット 2022-12-17 15 04 42" src="https://user-images.githubusercontent.com/111218880/208227998-c3a67cb7-96e6-42a2-b8f7-8d6b9c576c70.png">

## 実際の使用動画
https://user-images.githubusercontent.com/111218880/213861916-7abac2ad-f981-40dc-af4d-28deef83744b.mp4

## 機能紹介1:  簡単に気温と最適な服装を知る事ができる
- 現在地を選択すると天候・気温・適切な服装を提示します
- 気温情報取得には、天気予報のAPIを使用
- 現在地を選択できるため、外出先の情報も取得できます

### 参考: 服装の提案パターン
<img width="709" alt="スクリーンショット 2022-12-17 15 14 41" src="https://user-images.githubusercontent.com/111218880/208228247-96e6210c-fbd7-4ddd-84fb-0c108d36a28c.png">

## 機能紹介2:  他のユーザーの服をチェックできる
- 他のユーザーの服装の画像の取得ができます
- ログインすることで、服装の投稿へのいいね機能・自身の服装の投稿が利用できます
- 投稿時には、気温・ユーザー情報・画像をセットでデータベースに保存されます
- データベースに保存された画像を気温のパターンによって服装を提案します

### 参考: 投稿時のデータの保存の構成図
<img width="709" alt="スクリーンショット 2023-01-10 19 31 21" src="https://user-images.githubusercontent.com/111218880/211527886-857572c2-0b73-4cdf-9698-2c67af4fc496.png">


## 今後実装したいもの
- サイトにアクセスした時に、位置情報APIによって自動で位置情報を取得できるようにする
- マイページでユーザー情報を編集可能にする


