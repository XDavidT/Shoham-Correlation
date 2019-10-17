def HTML_Template(log_document):
    html = """\
    <html>
      <body>
      <div align="center">
        <p>
            <h1>We got important alert to let you know !</h1>
        </p>
        <p>
            Event X was active.<br>
            Please check device list: X
        </p>
           <br>
           Please check more details in Admin Panel !
        </div>
      </body>
    </html>
"""
    return html