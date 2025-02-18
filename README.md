# 起動方法

1. GitHubリポジトリをクローンする（https://github.com/musashi3814/task_app_backend.git）
2. 以下コードを実行する
    ```bash
    docker compose up
    ```

3. http://localhost:8000/docs へアクセスする


# ユーザータイプ

- user
    
    タスクのcrud権限（振られたタスクのみ）
    
- admin
    
    userの権限に加えて、ユーザーのcrud・タスクの全閲覧権限がある
    

# API仕様書

## 認証API (`/token`)

### 1. ログイン

**`POST /token/`**

### 概要

ユーザーがログインし、アクセストークン・IDトークン・リフレッシュトークンを取得する。

### リクエスト

- `username`: (string) メールアドレス
- `password`: (string) パスワード

### レスポンス

- `access_token`: (string) アクセストークン
- `id_token`: (string) IDトークン
- `refresh_token`: (string) リフレッシュトークン

### ステータスコード

- `200 OK`: 正常に認証成功
- `404 Not Found`: ユーザーが見つからない / 認証情報が正しくない
- `401 Unauthorized`: ユーザーが非アクティブ

---

### 2. トークンリフレッシュ

**`POST /token/refresh`**

### 概要

リフレッシュトークンを使用して新しいアクセストークンを取得する。

### リクエスト

- `refresh_token`: (string) リフレッシュトークン

### レスポンス

- `access_token`: (string) 新しいアクセストークン

### ステータスコード

- `200 OK`: 正常にアクセストークン発行
- `404 Not Found`: ユーザーが見つからない
- `401 Unauthorized`: ユーザーが非アクティブ

---

### 3. ユーザー登録

**`POST /token/signup`**

### 概要

新規ユーザー登録を行い、認証トークンを発行する。

### リクエスト

- `email`: (string) メールアドレス
- `password`: (string) パスワード
- `name`: (string) ユーザー名

### レスポンス

- `access_token`: (string) アクセストークン
- `id_token`: (string) IDトークン
- `refresh_token`: (string) リフレッシュトークン

### ステータスコード

- `201 Created`: ユーザー登録成功

---

### 注意事項

- サインアウトはフロント側で行う想定
- ユーザー登録なしでも以下アカウントでログインできる
    - username: test@example.com
    - password: testtest
- swaggerでの動作確認の際は、ユーザー登録した後、再度作成したアカウントでログインする必要がある（実際はフロント側でトークンを保持するため再度ログインは不要）

## タスクAPI (`/tasks`)

### 1. タスク作成

**`POST /tasks/`**

### 概要

新しいタスクを作成する。

### リクエスト

- `title`: (string) タスクのタイトル
- `description`: (string) タスクの詳細
- `due_date`: (datetime) タスク完了日時
- `status_id`: (0~2) タスクのステータス（未着手、進行中、完了）
- `priority_id`: (0~2) タスクの優先度（低、中、高）
- `assigned_id`: (list[integer]) タスクの担当者

### レスポンス

- `id`: (integer) タスクID
- `title`: (string) タスクのタイトル
- `description`: (string) タスクの詳細
- `due_date`: (datetime) タスク完了日時
- `status_id`: (0~2) タスクのステータス（未着手、進行中、完了）
- `priority_id`: (0~2) タスクの優先度（低、中、高）
- `assigned_id`: (list[integer]) タスクの担当者
- `created_at`: (datetime) タスクの作成日時
- `created_by`: (integer) 作成者

### ステータスコード

- `201 Created`: タスク作成成功

---

### 2. タスク一覧取得

**`GET /tasks/`**

### 概要

ユーザーが作成したタスクの一覧を取得する。

一般ユーザーの場合は振られたタスクのみ表示され、管理者の場合は全てのタスクが表示される。

### リクエストパラメータ

- `skip`: (integer) 省略する件数 (デフォルト: 0)
- `limit`: (integer) 取得する最大件数 (デフォルト: 100)

### レスポンス

- taskのリスト
    - `id`: (integer) タスクID
    - `title`: (string) タスクのタイトル
    - `due_date`: (datetime) タスク完了日時
    - `status_id`: (0~2) タスクのステータス
    - `status`: (string) タスクのステータス（未着手、進行中、完了）
    - `priority_id`: (0~2) タスクの優先度
    - `priority`: (string) タスクのステータス（未着手、進行中、完了）

### ステータスコード

- `200 OK`: 正常に取得

---

### 3. タスク詳細取得

**`GET /tasks/{task_id}`**

### 概要

指定したタスクの詳細情報を取得する。

一覧に加えて、タスク説明、タスク担当者、作成日時、作成者が表示される。

### リクエストパラメータ

- `task_id`: (int) 取得するタスクのID

### レスポンス

- `id`: (integer) タスクID
- `title`: (string) タスクのタイトル
- `description`: (string) タスクの詳細
- `due_date`: (datetime) タスク完了日時
- `status_id`: (0~2) タスクのステータス（未着手、進行中、完了）
- `priority_id`: (0~2) タスクの優先度（低、中、高）
- `assigned_id`: (list[integer]) タスクの担当者
- `created_at`: (datetime) タスクの作成日時
- `created_by`: (integer) 作成者

### ステータスコード

- `200 OK`: 正常に取得

---

### 4. タスク更新

**`PUT /tasks/{task_id}`**

### 概要

指定したタスクの内容を更新する。

### リクエスト

全て任意

- `title`: (string) タスクのタイトル
- `description`: (string) タスクの詳細
- `due_date`: (datetime) タスク完了日時
- `status_id`: (0~2) タスクのステータス（未着手、進行中、完了）
- `priority_id`: (0~2) タスクの優先度（低、中、高）
- `assigned_id`: (list[integer]) タスクの担当者

### レスポンス

- `id`: (integer) タスクID
- `title`: (string) タスクのタイトル
- `description`: (string) タスクの詳細
- `due_date`: (datetime) タスク完了日時
- `status_id`: (0~2) タスクのステータス（未着手、進行中、完了）
- `priority_id`: (0~2) タスクの優先度（低、中、高）
- `assigned_id`: (list[integer]) タスクの担当者
- `created_at`: (datetime) タスクの作成日時
- `created_by`: (integer) 作成者

### ステータスコード

- `200 OK`: 更新成功

---

### 5. タスク削除

**`DELETE /tasks/{task_id}`**

### 概要

指定したタスクを削除する。

### リクエストパラメータ

- `task_id`: (int) 削除するタスクのID

### ステータスコード

- `204 No Content`: 削除成功

---

## ユーザーAPI (`/user`)

### 1. ユーザー作成

**`POST /user/`**

### 概要

新しいユーザーを作成する（管理者のみ）。

### リクエスト

- `email`: (string) メールアドレス
- `password`: (string) パスワード
- `name`: (string) ユーザー名
- `is_active`: (string) 有効フラグ
- `is_admin`: (string) 管理者フラグ

### ステータスコード

- `201 Created`: ユーザー作成成功

---

### 2. ユーザー一覧取得

**`GET /user/`**

### 概要

登録されている全ユーザーの情報を取得する（管理者のみ）。

### リクエストパラメータ

- `skip`: (int) 省略する件数 (デフォルト: 0)
- `limit`: (int) 取得する最大件数 (デフォルト: 100)

### ステータスコード

- `200 OK`: 正常に取得

---

### 3. 自分の情報取得

**`GET /user/me`**

### 概要

現在ログインしているユーザーの情報を取得する。

### ステータスコード

- `200 OK`: 正常に取得

---

### 4. 自分の情報更新

**`PUT /user/me`**

### 概要

現在ログインしているユーザーの情報を更新する。

### ステータスコード

- `200 OK`: 更新成功

---

### 5. ユーザー詳細情報取得

**`GET /user/{user_id}`**

### 概要

指定したユーザーの詳細を取得する（管理者のみ）。

### ステータスコード

- `200 OK`: 更新成功

---

### 6. ユーザー情報更新

**`PUT /user/{user_id}`**

### 概要

指定したユーザーの情報を更新する（管理者のみ）。

### ステータスコード

- `200 OK`: 更新成功

---

### 7. ユーザー削除

**`DELETE /user/{user_id}`**

### 概要

指定したユーザーを削除する（管理者のみ）。

### リクエストパラメータ

- `user_id`: (int) 削除するユーザーのID

### ステータスコード

- `204 No Content`: 削除成功

# 工夫した点
- ユーザーのCRUD処理を追加し、ユーザータイプによってタスクの閲覧スコープを変えた
- Eager loadingを採用し、少ないクエリ数
- タスクのステータスと優先度を追加
- 


# 所要時間

- **環境構築**: 1
- **DB設計**: 0.75
- **API設計**: 1
- **Model実装**: 0.5
- **View実装**: 1
- **CRUD実装**: 7
    - User: 3
    - Task: 4
- **認証&認可実装**: 1
- **バリデーション**: 0.75
- **仕様書作成**: 0.5

    合計: 13.5時間

