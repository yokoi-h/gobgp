# policy調査

## bgp-policy.yang

#### augment
- bgp向けのpolicyとして使えるmatchやactionはbgp-policy.yangで定義されており、augment命令(?)によって、その配下のnodeがrouting-policy.yang側の指定されたnodeに組み込まれる

```
  augment "/rpol:routing-policy/rpol:defined-sets" {
    description "adds BGP defined sets container to routing policy
    model";

    container bgp-defined-sets {
      description
        "BGP-related set definitions for policy match conditions";

      list community-set {
        key community-set-name;
        description
            "Definitions for community sets";

        leaf community-set-name {
          type string;
          mandatory true;
          description
            "name / label of the community set -- this is used to
            reference the set in match conditions";
        }

        leaf-list community-members {
          type union {
            type bgp-std-community-type;
            type bgp-community-regexp-type;
            type bgp-well-known-community-type;
          }
          description
            "members of the community set";
        }

      }
...
```

----

## 必要なmatch条件

### as-path list
- *(正規表現での設定が望ましい）もし不可能であればas-originのみでもひとまず可*

1. ---> bgp-defined-sets/as-path-set/as-path-set-membersでmatchさせるas_pathを指定する


#### bgp-defined-sets/as-path-set
- ---> bgp-defined-sets/as-path-set/as-path-set-membersは型がstringであるため、独自にsyntaxを決めれば、正規表現も扱えるはず

```
  augment "/rpol:routing-policy/rpol:defined-sets" {
    description "adds BGP defined sets container to routing policy
    model";

    container bgp-defined-sets {
      description
        "BGP-related set definitions for policy match conditions";


    ...


      list as-path-set {
        key as-path-set-name;
        description
            "Definitions for AS path sets";

        leaf as-path-set-name {
          type string;
          description
            "name of the AS path set -- this is used to reference the
            the set in match conditions";
        }

        leaf-list as-path-set-members {
          // TODO: need to refine typedef for AS path expressions
          type string;
          description
              "AS path expression -- list of ASes in the set";
        }
      }

    ...
```


2. ---> bgp-match-conditions/match-as-path-setコンテナの中で、bgp-defined-sets/as-path-set/as-path-set-nameで付与した名前を指定する

#### bgp-match-conditions/match-as-path-set
```
  grouping bgp-match-conditions {
    description
      "Condition statement definitions for checking membership in a
      defined set";

     ...

    container match-as-path-set {
      presence
        "The presence of this container indicates that the route
        should match the referenced as-path set";

      description
        "Match a referenced as-path set according to the logic
        defined in the match-set-options leaf";

      leaf as-path-set {
      # ここでbgp-defined-sets/as-path-setで指定した名前を設定すると、conditionとして利用可能
        type leafref {
          path "/rpol:routing-policy/rpol:defined-sets/" +
            "bgp-pol:bgp-defined-sets/bgp-pol:as-path-set/" +
            "bgp-pol:as-path-set-name";
          require-instance true;
        }
        description "References a defined AS path set";
      }
      uses rpol:match-set-options-group;
    }
  }
```
----


### prefix list (exact match or orlonger)
- *現状exact matchでOKだがorlongerもほしい ex) 1.0.0.0/24 orlonger /28*

1. ---> 今の実装で指定可能と思われます。

```
[[DefinedSets.PrefixSetList]]
PrefixSetName = "ps1"
[[DefinedSets.PrefixSetList.PrefixList]]
Address = "1.0.0.0"
Masklength = 24
MasklengthRange = "24...28"
```

----


### community list
- *現状standard communityのみでOKだがextended communityでのマッチもほしい*


1. ---> bgp-defined-sets/community-set/community-membersで、条件となるcommunity群を指定する
2. ---> extended communityも同様に、bgp-defined-sets/ext-community-set/ext-community-membersで、条件となるcommunity群を指定する

#### bgp-defined-sets/community-set, ext-community-set
```
  augment "/rpol:routing-policy/rpol:defined-sets" {
    description "adds BGP defined sets container to routing policy
    model";

    container bgp-defined-sets {
      description
        "BGP-related set definitions for policy match conditions";

      list community-set {
        key community-set-name;
        description
            "Definitions for community sets";

        leaf community-set-name {
          type string;
          mandatory true;
          description
            "name / label of the community set -- this is used to
            reference the set in match conditions";
        }

        leaf-list community-members {
          type union {
            type bgp-std-community-type;            #  standard commmunity attributes
            type bgp-community-regexp-type;         #  正規表現
            type bgp-well-known-community-type;     #  NO_EXPORTなど標準的なもの
          }
          description
            "members of the community set";
        }

      }

      list ext-community-set {
        key ext-community-set-name;
        description
            "Definitions for extended community sets";

        leaf ext-community-set-name {
          type string;
          description
            "name / label of the extended community set -- this is
            used to reference the set in match conditions";
        }

        leaf-list ext-community-members {
          type union {
            type bgp-ext-community-type;
            // TODO: is regexp support needed for extended
            // communities?
            type bgp-community-regexp-type;
          }
          description
              "members of the extended community set";
        }
      }
...
```


1. ---> bgp-match-conditions/match-community-set/community-setに、bgp-defined-setsコンテナ内で定義した、community-setの名前(community-set-name)を指定する。
2. ---> extended−communityの場合は、match-ext-community-setにext-community-setの名前を指定する。


#### bgp-match-conditions/match-community-set
```
  grouping bgp-match-conditions {
    description
      "Condition statement definitions for checking membership in a
      defined set";

    container match-community-set {
      presence
        "The presence of this container indicates that the routes
        should match the referenced community-set";

      description
        "Match a referenced community-set according to the logic
        defined in the match-set-options leaf";

      leaf community-set {　　# ここにbgp-defined-setsコンテナ内で定義した、community-setの名前(community-set-name)を指定する
        type leafref {
          path "/rpol:routing-policy/rpol:defined-sets/" +
            "bgp-pol:bgp-defined-sets/bgp-pol:community-set/" +
            "bgp-pol:community-set-name";
          require-instance true;
        }
        description
          "References a defined community set";
      }
      uses rpol:match-set-options-group;
    }

    container match-ext-community-set {
      presence
        "The presence of this container indicates that the routes
        should match the referenced extended community set";

      description
        "Match a referenced extended community-set according to the
        logic defined in the match-set-options leaf";

      leaf ext-community-set {  # ここにbgp-defined-setsコンテナ内で定義した、ext−community-setの名前(ext-community-set-name)を指定する
        type leafref {
          path "/rpol:routing-policy/rpol:defined-sets/" +
            "bgp-pol:bgp-defined-sets/bgp-pol:ext-community-set/" +
            "bgp-pol:ext-community-set-name";
          require-instance true;
        }
        description "References a defined extended community set";
      }
      uses rpol:match-set-options-group;
    }

  }
```

----

### as-pathの数
- *ex.)AS-PATHのAS数が256個以上はdenyなど。*

1. ---> bgp-attribute-conditions/as-path-lengthの先の、attribute-compare-operatorsで個数を指定する

#### bgp-attribute-conditions/as-path-length

```
  grouping bgp-attribute-conditions {
    description
      "Condition statement definitions for comparing a BGP route
      attribute to a specified value";

  ...

    container as-path-length {

      presence "node is present in the config data to indicate a
      as-path-length condition";

      description
        "Value and comparison operations for conditions based on the
        length of the AS path in the route update";

      uses pt:attribute-compare-operators;
    }
  }
```

#### pt:attribute-compare-operators

```
  grouping attribute-compare-operators {
    description "common definitions for comparison operations in
    condition statements";

    leaf operator {
        type identityref {
          base attribute-comparison;
        }
        description
          "type of comparison to be performed";
      }

    leaf value {
      type uint32;
      description
        "value to compare with the community count";
    }
  }
```


----

### peer ip（優先度低）
- *ex.)該当ピアから聞こえてきたBGP経路に対して適用*

1. ---> 今の実装でも条件の指定が可能ですが、prefixとneighborを同時に指定するようになっており、neighborの条件のみをpolicyに定義するための修正が必要と思われます。
```
# example 1
[[DefinedSets.NeighborSetList]]
NeighborSetName = "ns1"
[[DefinedSets.NeighborSetList.NeighborInfoList]]
Address = "10.0.255.1"
```

----

## 必要なaction

### set med [N|+N|-N|igp]

1. ---> bgp-actions/set-medでmedにセットする値を指定する。
2. ---> 値は、bgp-set-med-type型だが、string型にして、演算子も含めて定義できるようにしておけばよさそう

#### bgp-actions/set-med

```
  augment "/rpol:routing-policy/rpol:policy-definition/" +
    "rpol:statement/rpol:actions" {
    description "BGP policy actions added to routing policy
    module";

    container bgp-actions {
      description
        "Definitions for policy action statements that
        change BGP-specific attributes of the route";

  ...
        leaf set-med {
          type bgp-set-med-type;
          description "set the med metric attribute in the route
          update";


```

#### set−med−type
```
  typedef bgp-set-med-type {
    type union {
      type uint32;
      type enumeration {
        enum IGP {
          description "set the MED value to the IGP cost toward the
          next hop for the route";
        }
      }
    }
    description "type definition for specifying how the BGP MED can
    be set in BGP policy actions";
  }
```

----

### set as-path prepend [XXXX N|last-as N]

- *XXXX N: 該当経路のAS_PATH attr.にASXXXXをN回prepend*
- *last-as N: 該当経路のAS_PATH attr.にそのAS_PATHの最左(last-as)をN回prepend*

1. ---> bgp-actions/set-as-path-prependrepeat-nでas-pathにセットする回数を指定するようだが、自分のAS番号を挿入する想定のよう
2. ---> 任意のAS番号もしくは最左のASを付加できるように拡張する必要あり

#### bgp-actions/set-as-path-prepend

```
  augment "/rpol:routing-policy/rpol:policy-definition/" +
    "rpol:statement/rpol:actions" {
    description "BGP policy actions added to routing policy
    module";

    container bgp-actions {
      description
        "Definitions for policy action statements that
        change BGP-specific attributes of the route";

  ...
      container set-as-path-prepend {

        presence "node is pesent in the config data to use the AS
      prepend action";
        description
            "action to prepend local AS number to the AS-path a
        specified number of times";

        leaf repeat-n {
          type uint8;
          description "number of times to prepend the local AS
          number";
        }
      }


```

----

### set community AA:NN...

- *該当経路のCOMMUNITY attr.にAA:NNを追加（複数設定可）*
- *とりあえずはstandard communityのみで可将来的にはextended communityも*

1. ---> bgp-actions/set-community/set-community-method、またはset-ext-community/set-ext-community-methodで指定する付加するcommunityを指定する
2. ---> leaf-list communitiesと書いてある行があるので、複数設定もできる模様
3. ---> leaf optionsで追加や削除等を指定可能

#### bgp-actions/set-community, set-ext-community

```
  augment "/rpol:routing-policy/rpol:policy-definition/" +
    "rpol:statement/rpol:actions" {
    description "BGP policy actions added to routing policy
    module";

    container bgp-actions {
      description
        "Definitions for policy action statements that
        change BGP-specific attributes of the route";

  ...
      container set-community {
        presence "node is present in the config data when
        set-community action is used";
        description
          "action to set the community attributes of the route, along
          with options to modify how the community is modified";

        choice set-community-method {
          description
            "Option to set communities using an inline list or
            reference to an existing defined set.";

          case inline {
            leaf-list communities {
              type union {
                type bgp-std-community-type;
                type bgp-well-known-community-type;
              }
              description
                "Set the community values for the update inline with
                a list.";
            }
          }
          case reference {
            leaf community-set-ref {
              type leafref {
                path "/rpol:routing-policy/rpol:defined-sets/" +
                  "bgp-pol:bgp-defined-sets/bgp-pol:community-set/" +
                  "bgp-pol:community-set-name";
                require-instance true;
              }
              description
                "References a defined community set by name";
            }
          }
        }
        leaf options {
          type bgp-set-community-option-type;
          description
            "Options for modifying the community attribute with
            the specified values.  These options apply to both
            methods of setting the community attribute.";
        }
      }

      container set-ext-community {

        presence "node is present in the config data when
        set-community action is used";
        description
          "Action to set the extended community attributes of the
          route, along with options to modify how the community is
          modified";

        choice set-ext-community-method {
          description
            "Option to set communities using an inline list or
            reference to an existing defined set.";

          case inline {
            leaf-list communities {
              type union {
                type bgp-ext-community-type;
                type bgp-well-known-community-type;
              }
              description
                "Set the community values for the update inline with
                a list.";
            }
          }
          case reference {
            leaf ext-community-set-ref {
              type leafref {
                path "/rpol:routing-policy/rpol:defined-sets/" +
                  "bgp-pol:bgp-defined-sets/" +
                  "bgp-pol:ext-community-set/" +
                  "bgp-pol:ext-community-set-name";
                require-instance true;
              }
              description
                "References a defined extended community set by
                name";
            }
          }
        }
        leaf options {
          type bgp-set-community-option-type;
          description
            "options for modifying the extended community
            attribute with the specified values. These options
            apply to both methods of setting the community
            attribute.";
        }
      }
```


#### bgp-set-community-option-type

```
  typedef bgp-set-community-option-type {
    type enumeration {
      enum ADD {
        description
          "add the specified communities to the existing
          community attribute";
      }
      enum REMOVE {
        description
          "remove the specified communities from the
          existing community attribute";
      }
      enum REPLACE {
        description
          "replace the existing community attribute with
          the specified communities. If an empty set is
          specified, this removes the community attribute
          from the route.";
      }
    }
    description
      "Type definition for options when setting the community
      attribute in a policy action";
  }
```

----

- bgp-policy.yang側で定義されたmatchに相当するbgp-conditionsと、actionに相当するbgp-actionsは、**augment**によって、routing−policy.yang側の[routing−policyコンテナ](https://github.com/openconfig/yang/blob/master/experimental/openconfig/policy/routing-policy.yang#L400)に組み込まれる。

