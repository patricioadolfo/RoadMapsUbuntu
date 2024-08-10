#~Layout with Sample Tools
Generated using [DbSchema](https://dbschema.com)




### ~Layout with Sample Tools
![img](./~LayoutwithSampleTools.svg)



### Table Default.auth_group 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  &#11019; | id| INTEGER AUTOINCREMENT |
| * &#128269; | name| VARCHAR(150)  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_auth\_group | ON id|
| &#128269;  | unq\_auth\_group\_name | ON name|



### Table Default.auth_group_permissions 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | id| INTEGER AUTOINCREMENT |
| * &#128269; &#11016; | group\_id| INTEGER  |
| * &#128269; &#11016; | permission\_id| INTEGER  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_auth\_group\_permissions | ON id|
| &#128269;  | auth\_group\_permissions\_group\_id\_permission\_id\_0cd325b0\_uniq | ON group\_id, permission\_id|
| &#128270;  | auth\_group\_permissions\_group\_id\_b120cbf9 | ON group\_id|
| &#128270;  | auth\_group\_permissions\_permission\_id\_84c5c92e | ON permission\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( group\_id ) ref [Default.auth\_group](#auth\_group) (id) |
|  | Fk | ( permission\_id ) ref [Default.auth\_permission](#auth\_permission) (id) |




### Table Default.auth_permission 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  &#11019; | id| INTEGER AUTOINCREMENT |
| * &#128269; &#11016; | content\_type\_id| INTEGER  |
| * &#128269; | codename| VARCHAR(100)  |
| * | name| VARCHAR(255)  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_auth\_permission | ON id|
| &#128269;  | auth\_permission\_content\_type\_id\_codename\_01ab375a\_uniq | ON content\_type\_id, codename|
| &#128270;  | auth\_permission\_content\_type\_id\_2f476e4b | ON content\_type\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( content\_type\_id ) ref [Default.django\_content\_type](#django\_content\_type) (id) |




### Table Default.auth_user 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  &#11019; | id| INTEGER AUTOINCREMENT |
| * | password| VARCHAR(128)  |
|  | last\_login| DATETIME  |
| * | is\_superuser| BOOLEAN  |
| * &#128269; | username| VARCHAR(150)  |
| * | last\_name| VARCHAR(150)  |
| * | email| VARCHAR(254)  |
| * | is\_staff| BOOLEAN  |
| * | is\_active| BOOLEAN  |
| * | date\_joined| DATETIME  |
| * | first\_name| VARCHAR(150)  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_auth\_user | ON id|
| &#128269;  | unq\_auth\_user\_username | ON username|



### Table Default.auth_user_groups 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | id| INTEGER AUTOINCREMENT |
| * &#128269; &#11016; | user\_id| INTEGER  |
| * &#128269; &#11016; | group\_id| INTEGER  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_auth\_user\_groups | ON id|
| &#128269;  | auth\_user\_groups\_user\_id\_group\_id\_94350c0c\_uniq | ON user\_id, group\_id|
| &#128270;  | auth\_user\_groups\_user\_id\_6a12ed8b | ON user\_id|
| &#128270;  | auth\_user\_groups\_group\_id\_97559544 | ON group\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( user\_id ) ref [Default.auth\_user](#auth\_user) (id) |
|  | Fk | ( group\_id ) ref [Default.auth\_group](#auth\_group) (id) |




### Table Default.auth_user_user_permissions 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | id| INTEGER AUTOINCREMENT |
| * &#128269; &#11016; | user\_id| INTEGER  |
| * &#128269; &#11016; | permission\_id| INTEGER  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_auth\_user\_user\_permissions | ON id|
| &#128269;  | auth\_user\_user\_permissions\_user\_id\_permission\_id\_14a6b632\_uniq | ON user\_id, permission\_id|
| &#128270;  | auth\_user\_user\_permissions\_user\_id\_a95ead1b | ON user\_id|
| &#128270;  | auth\_user\_user\_permissions\_permission\_id\_1fbb5f2c | ON permission\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( user\_id ) ref [Default.auth\_user](#auth\_user) (id) |
|  | Fk | ( permission\_id ) ref [Default.auth\_permission](#auth\_permission) (id) |




### Table Default.django_admin_log 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | id| INTEGER AUTOINCREMENT |
|  | object\_id| TEXT  |
| * | object\_repr| VARCHAR(200)  |
| * | action\_flag| SMALLINT UNSIGNED  |
| * | change\_message| TEXT  |
| &#128270; &#11016; | content\_type\_id| INTEGER  |
| * &#128270; &#11016; | user\_id| INTEGER  |
| * | action\_time| DATETIME  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_django\_admin\_log | ON id|
| &#128270;  | django\_admin\_log\_content\_type\_id\_c4bce8eb | ON content\_type\_id|
| &#128270;  | django\_admin\_log\_user\_id\_c564eba6 | ON user\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( content\_type\_id ) ref [Default.django\_content\_type](#django\_content\_type) (id) |
|  | Fk | ( user\_id ) ref [Default.auth\_user](#auth\_user) (id) |


##### Constraints
|Name |Definition |
|---|---|
| Cns_django_admin_log_action_flag | "action\_flag" &gt;= 0 |




### Table Default.django_content_type 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  &#11019; | id| INTEGER AUTOINCREMENT |
| * &#128269; | app\_label| VARCHAR(100)  |
| * &#128269; | model| VARCHAR(100)  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_django\_content\_type | ON id|
| &#128269;  | django\_content\_type\_app\_label\_model\_76bd3d3b\_uniq | ON app\_label, model|



### Table Default.django_migrations 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | id| INTEGER AUTOINCREMENT |
| * | app| VARCHAR(255)  |
| * | name| VARCHAR(255)  |
| * | applied| DATETIME  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_django\_migrations | ON id|



### Table Default.django_session 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | session\_key| VARCHAR(40)  |
| * | session\_data| TEXT  |
| * &#128270; | expire\_date| DATETIME  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_django\_session | ON session\_key|
| &#128270;  | django\_session\_expire\_date\_a5c62663 | ON expire\_date|



### Table Default.route_nodedestination 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  &#11019; | id| INTEGER AUTOINCREMENT |
| * | name| VARCHAR(100)  |
| * | address| VARCHAR(100)  |
| * &#128269; | phoneNumber| VARCHAR(16)  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_route\_nodedestination | ON id|
| &#128269;  | unq\_route\_nodedestination\_phoneNumber | ON phoneNumber|



### Table Default.route_nodeorigin 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  &#11019; | id| INTEGER AUTOINCREMENT |
| * | name| VARCHAR(100)  |
| * | address| VARCHAR(100)  |
| * &#128269; | phoneNumber| VARCHAR(16)  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_route\_nodeorigin | ON id|
| &#128269;  | unq\_route\_nodeorigin\_phoneNumber | ON phoneNumber|



### Table Default.route_perfil 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | id| INTEGER AUTOINCREMENT |
| &#128270; &#11016; | user\_id| INTEGER  |
| &#128270; &#11016; | nodo\_id| BIGINT  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_route\_perfil | ON id|
| &#128270;  | route\_perfil\_user\_id\_5cbfb039 | ON user\_id|
| &#128270;  | route\_perfil\_nodo\_id\_86ac1ade | ON nodo\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( user\_id ) ref [Default.auth\_user](#auth\_user) (id) |
|  | Fk | ( nodo\_id ) ref [Default.route\_nodedestination](#route\_nodedestination) (id) |




### Table Default.route_route 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  &#11019; | id| INTEGER AUTOINCREMENT |
| * | description| TEXT  |
|  | preparation\_date| DATE  |
| &#128270; &#11016; | destination\_id| BIGINT  |
| &#128270; &#11016; | origin\_id| BIGINT  |
| * | status| VARCHAR(1)  |
| &#128270; &#11016; | user\_id| INTEGER  |
|  | preparation\_time| TIME  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_route\_route | ON id|
| &#128270;  | route\_route\_destination\_id\_d86b7481 | ON destination\_id|
| &#128270;  | route\_route\_origin\_id\_55bb5bc6 | ON origin\_id|
| &#128270;  | route\_route\_user\_id\_928ac66d | ON user\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( destination\_id ) ref [Default.route\_nodedestination](#route\_nodedestination) (id) |
|  | Fk | ( origin\_id ) ref [Default.route\_nodeorigin](#route\_nodeorigin) (id) |
|  | Fk | ( user\_id ) ref [Default.auth\_user](#auth\_user) (id) |




### Table Default.route_routeinstance 
|Idx |Name |Data Type |
|---|---|---|
| * &#128273;  | id| CHAR(32)  |
| * | status| VARCHAR(1)  |
| &#128270; &#11016; | route\_id| BIGINT  |
|  | instance\_date| DATE  |
| &#128270; &#11016; | user\_id| INTEGER  |
|  | instance\_time| TIME  |


##### Indexes 
|Type |Name |On |
|---|---|---|
| &#128273;  | pk\_route\_routeinstance | ON id|
| &#128270;  | route\_routeinstance\_route\_id\_87e9eabe | ON route\_id|
| &#128270;  | route\_routeinstance\_user\_id\_1c37a60a | ON user\_id|

##### Foreign Keys
|Type |Name |On |
|---|---|---|
|  | Fk | ( route\_id ) ref [Default.route\_route](#route\_route) (id) |
|  | Fk | ( user\_id ) ref [Default.auth\_user](#auth\_user) (id) |





