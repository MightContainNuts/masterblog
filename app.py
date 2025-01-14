import json

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BLOG_DATA = "blog_data.json"


def open_json():
    try:
        with open(BLOG_DATA, "r") as read_handle:
            local_data = json.load(read_handle)
            if not local_data:
                return []
        return local_data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print("oops, exception handled", e)


def write_json(local_data):
    try:
        with open(BLOG_DATA, "w") as write_handler:
            json.dump(local_data, write_handler, indent=4)
            print(f"Data successfully written to JSON file. {write_handler}")
    except (FileNotFoundError, Exception) as e:
        print("Exception caught", e)


def get_post(post_id: int):
    posts = open_json()
    selected_post = next((post for post in posts if post["id"] == post_id),
                         None)
    return selected_post


@app.route("/")
def index():
    posts = open_json()
    if posts:
        return render_template("index.html", posts=posts)
    else:
        return "oops, error"


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        local_storage = open_json()
        current_id = max(blog["id"] for blog in local_storage)
        new_id = current_id + 1
        new_blog = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
        }
        local_storage.append(new_blog)
        write_json(local_storage)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    posts = open_json()
    post_to_delete = next((post for post in posts if post["id"] == post_id),
                          None)

    if post_to_delete:
        posts.remove(post_to_delete)
        print(f"Deleting {post_to_delete}")
        write_json(posts)
    else:
        print(f"Post not found with id: {post_id}")

    return redirect(url_for("index"))


@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    posts = open_json()
    post_to_like = next((post for post in posts if post["id"] == post_id),
                        None)
    print(post_to_like)
    if post_to_like:
        post_to_like["likes"] = post_to_like.get("likes", 0) + 1
        write_json(posts)
        print("finished writing to file")
        print(post_to_like)
        print(posts)
    return redirect((url_for("index")))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update_post(post_id):
    posts = open_json()
    post_to_update = next((post for post in posts if post["id"] == post_id),
                          None)
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        posts = open_json()
        post_to_update["title"] = title
        post_to_update["author"] = author
        post_to_update["content"] = content
        write_json(posts)
        if post_to_update:
            return redirect(url_for("index"))
    return render_template("update.html",
                           post_to_update=post_to_update)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
