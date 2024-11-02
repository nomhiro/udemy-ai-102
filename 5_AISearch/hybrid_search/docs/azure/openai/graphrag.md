# はじめに

今までのRAGは、ドキュメントをチャンク化して検索インデックスに格納し、クエリに対して検索、推論を行う といった手法でした。
この場合、ドキュメントのチャンク単位で検索され推論に使うため、ドキュメン卜横断で複雑な関係性に対し推論することには向いていないように思います。
GraphDBは、ドキュメントをノード（頂点）とリレーション（頂点間の関係性）に変換し、ドキュメント内の要素間の関係性を持つDBです。

以前に、LlamaIndexをベースにNeo4jへのナレッジグラフ生成を試してみましたが、日本語だと精度が落ちて実用には耐えられなさそうでした。

今回は、MicrosoftResearchからGraphDBのソリューションがGitHubで公開されたので、そちらを試してみます。

- GraphRagのGitHubリポジトリ
https://github.com/microsoft/graphrag

- GraphRag AcceleratorのGitHubリポジトリ
https://github.com/Azure-Samples/graphrag-accelerator


# まとめ
まず第一弾として、Microsoft Researchから提供されたGraphRAGを動かせるように環境構築しました。
Acceleratorが用意されているため、構築は非常に楽です。
txtデータ使ってIndexを構築し、2種類のクエリ「Global Query」と「Local Query」を実行し、それぞれの結果を確認しました。

動作確認をしただけで、ナレッジグラフを構築する部分の処理詳細や、GlobalQueryとLocalQueryがどのような処理で実行されているのか、まだ追えていませんので、そちらはいずれ整理します。

**また、このようなGraphRAGを使うときに課題だと感じていたのが、元データが追加/更新/削除された時のGraphデータの追従です。** この点についても、今後検証していきたいと思います。

次回の第二弾では、GraphRAGにAPIが用意されているためそれらを利用して、GraphRAGの動きを確認してみます。
