## yangのlistに対する構造体のメンバ名について


現状、yangのnodeでlistとして定義されているものは、bgp-config.goの構造体のメンバ名としてListというsuffixをつけており、

例えば、yang上のlist neighborの部分、

```
    list neighbor {
      key "neighbor-address";
      description
        "List of BGP peers, uniquely identified by neighbor
        address.";
      leaf neighbor-address {
        type inet:ip-address;
        description
          "Address of the BGP peer, either IPv4 or IPv6.";
      }

      leaf peer-as {
        type inet:as-number;
        mandatory "true";
        description
          "AS number of the peer.";

      }
      uses bgp-common-configuration;
      uses bgp-mp:address-family-configuration;
      uses bgp-group-neighbor-common-configuration;
      uses bgp-op:bgp-op-neighbor-group;
    }
```

は、構造体の要素名として

```go
type Bgp struct {
	// original -> bgp:global
	Global Global
	// original -> bgp:peer-group
	PeerGroupList []PeerGroup
	// original -> bgp:neighbor
	NeighborList []Neighbor                      // <-- Listの部分
	// original -> rpol:apply-policy
	ApplyPolicy ApplyPolicy
}
```
という宣言をしています。

これをtomlに落とした場合、
```
[[NeighborList]]
  NeighborAddress = "192.168.31.171"
  PeerAs = 65001
  Description = ""
	...
```

となるのですが、ひとつのneighborの情報を定義する場所で、NeighborListという名前が付いているのも設定ファイルとしてはわかりにくいと感じています。
<br>
逆にListがないとtoml上では以下のようになり、わかりやすくなると思います。

```
[[Neighbor]]
  NeighborAddress = "192.168.31.171"
  PeerAs = 65001
  Description = ""
	...
```

toml上で"List"をなくすためには、構造体のメンバ名を型宣言と同じ文字列に変更する必要があり、
以下のように配列の型宣言とメンバ名を同じ文字列にすることになります。

可読性は落ちますが、コンパイル時に怒られることはないようです。

```go
type Bgp struct {
	// original -> bgp:global
	Global Global
	// original -> bgp:peer-group
	PeerGroupList []PeerGroup
	// original -> bgp:neighbor
	Neighbor []Neighbor     //メンバ名のListを除去
	// original -> rpol:apply-policy
	ApplyPolicy ApplyPolicy
}
```

そもそも、Listをつけてしまったのがそもそもよくなかったようです。
設定ファイルをわかりやすくするという意味で、メンバ名からListを省いた方がよいかと思っているのですが、いかがでしょうか。
(ドキュメントなど波及範囲は広いので慎重に修正する必要はありますが。)


Policyの設定も、Listを省いた方が、tomlでの見え方もわかりやすくなると思います。

```
[[PolicyDefinition]]
  Name = "pd1"

  [[PolicyDefinition.Statement]]
    Name = "statement1"
    [PolicyDefinition.Statement.Conditions]
      CallPolicy = ""
      MatchPrefixSet = "ps1"
      MatchNeighborSet = "ns1"
      MatchSetOptions = 1
      InstallProtocolEq = 0
      [PolicyDefinitionList.Statement.Conditions.IgpConditions]
        TagEq = ""
    [PolicyDefinition.Statement.Actions]
      AcceptRoute = false
      RejectRoute = true
      [PolicyDefinitionList.Statement.Actions.IgpActions]
        SetTag = ""
```

構造体でListをつけたまま(今の状態)だと、以下のようになります。
```
[[PolicyDefinitionList]]
  Name = "pd3"

  [[PolicyDefinitionList.StatementList]]
    Name = "statement1"
    [PolicyDefinitionList.StatementList.Conditions]
      CallPolicy = ""
      MatchPrefixSet = "ps3"
      MatchNeighborSet = "ns1"
      MatchSetOptions = 1
      InstallProtocolEq = 0
      [PolicyDefinitionList.StatementList.Conditions.IgpConditions]
        TagEq = ""
    [PolicyDefinitionList.StatementList.Actions]
      AcceptRoute = false
      RejectRoute = true
      [PolicyDefinitionList.StatementList.Actions.IgpActions]
        SetTag = ""
```

