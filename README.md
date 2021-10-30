# The Null Pointer

This is a no-bullshit file hosting and URL shortening service that also runs [mwt.sh](https://mwt.sh). It can be run on a shared hosting provider with [Passenger](https://help.dreamhost.com/hc/en-us/articles/215769578-Passenger-overview).

## Configuration

To change settings, modify `instance/config.py`. For more information on instance configuration, see [the Flask documentation](https://flask.palletsprojects.com/en/2.0.x/config/#instance-folders).

My `instance/config.py` file contains:

~~~py
FHOST_USE_X_ACCEL_REDIRECT = False
USE_X_SENDFILE = True
NSFW_DETECT = False
SQLALCHEMY_DATABASE_URI = "mysql://USER:PASSWORD@SQL_HOSTNAME/TABLE_NAME"
DIRECTORY = "/home/dh_user/mwt.sh/"
~~~

To customize the home and error pages, simply create a `templates` directory in your instance directory and copy any templates you want to modify there.

If you are running nginx, you should use the `X-Accel-Redirect` header. To make it work, include this in your nginx config’s `server` block:

~~~conf
location /up {
    internal;
}
~~~

where `/up` is whatever you’ve configured as `FHOST_STORAGE_PATH`.

For all other servers, set `FHOST_USE_X_ACCEL_REDIRECT` to `False` and `USE_X_SENDFILE` to `True`, assuming your server supports this. Apache requires `mod_xsendfile` to use this feature. Most shared hosts do not provide it by default. Dreamhost will provide it if you open a ticket. If you set both to `False`, Flask will serve the file with chunked encoding,  which sucks and should be avoided at all costs.

To make files expire, simply create a cronjob that runs `cleanup.py` every now and then.

Before running the service for the first time, run `FLASK_APP=fhost flask db upgrade`.

### Password Protection

This fork features password protection for the POST endpoint. This means the upload is impossible without basic authentication. Accounts are managed from a `.htpasswd` file. You can create your first user by running:

~~~sh
htpasswd -c -B -b .htpasswd user1 password
~~~

Once the file is created, you can append users with:

~~~sh
htpasswd -B -b .htpasswd user2 password
~~~

## NSFW Detection

0x0 supports classification of NSFW content via Yahoo’s open_nsfw Caffe neural network model. This works for images and video files and requires the following:

* Caffe Python module (built for Python 3)
* `ffmpegthumbnailer` executable in `$PATH`
