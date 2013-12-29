import webapp2
import logging
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class GetRes (blobstore_handlers.BlobstoreDownloadHandler):
  def get (self, resource):
      blob_info = blobstore.BlobInfo.get(resource)
      self.send_blob(blob_info)

class GetIcon (blobstore_handlers.BlobstoreDownloadHandler):
  def get (self, resource):
      blob_info = blobstore.BlobInfo.get(resource)
      self.send_blob(blob_info)
