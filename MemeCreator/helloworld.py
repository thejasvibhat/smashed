import webapp2

MAIN_PAGE_HTML = """\
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Meme Creator</title>
      <link rel="stylesheet" href="./MEMEHTML/jquery-ui.css" />
    <script src="./MEMEHTML/jquery.tools.min.js"></script>
  <!--script src="http://code.jquery.com/jquery-1.9.1.js"></script!-->
  <script src="./MEMEHTML/jquery-ui.js"></script>
    <link rel="stylesheet" href="./MEMEHTML/style.css"> 
    <link rel="stylesheet" href="./MEMEHTML/scrollable-buttons.css">   
    <link rel="stylesheet" href="./MEMEHTML/scrollable-horizontal.css">   
    <script  src="./MEMEHTML/meme.js"></script>
</head> 
<body>    
      
     <input type="file" id="myFile" style="display:none;">
 
<div class="backgroundClass" style="margin:0 auto;" >
    <div class="autoClass" align="center"> 
        <span class="textClass inlineBlock" style="font-weight:bold;color:#b9b9b9;">MEME CREATOR</span>
        <span class="textClass" style="font-size:20px;color:#b9b9b9;">&nbsp;&nbsp;Drag an image from image roller or upload new</span>
    </div> 
         
    <div style="margin:0 auto; width: 634px; height:120px;">
<!-- "previous page" action -->
<a class="prev browse left"></a>
 
<!-- root element for scrollable -->
<div class="scrollable" id="scrollable">
 
  <!-- root element for the items -->
  <div class="items">
 
    <!-- 1-5 -->
   
      <!--img src="http://farm1.static.flickr.com/143/321464099_a7cfcb95cf_t.jpg" />
      <img src="http://farm4.static.flickr.com/3089/2796719087_c3ee89a730_t.jpg" />
      <img src="http://farm1.static.flickr.com/79/244441862_08ec9b6b49_t.jpg" />
      <img src="http://farm1.static.flickr.com/28/66523124_b468cf4978_t.jpg" /-->
    
 
    <!-- 5-10 -->
    
      <!--img src="http://farm1.static.flickr.com/163/399223609_db47d35b7c_t.jpg" />
      <img src="http://farm1.static.flickr.com/135/321464104_c010dbf34c_t.jpg" />
      <img src="http://farm1.static.flickr.com/40/117346184_9760f3aabc_t.jpg" />
      <img src="http://farm1.static.flickr.com/153/399232237_6928a527c1_t.jpg" /-->
   
 
    <!-- 10-15 -->
   
      <!--img src="http://farm4.static.flickr.com/3629/3323896446_3b87a8bf75_t.jpg" />
      <img src="http://farm4.static.flickr.com/3023/3323897466_e61624f6de_t.jpg" />
      <img src="http://farm4.static.flickr.com/3650/3323058611_d35c894fab_t.jpg" />
      <img src="http://farm4.static.flickr.com/3635/3323893254_3183671257_t.jpg" /-->
    
 
  </div>  
 
</div>
 
<!-- "next page" action -->
<a class="next browse right"></a>
</div>
<table class="Main" width="1000" height="800" style="align:center;border:solid;" >
   <tr width="100%" height="100%"  >
        <td width="50%" height="100%"  style="border:solid;">
            
            <div id="BaseCanvas"  class="layout_canvasClass  style_canvasClass displayBlock" >
                <img id="backImage" class="displayBlock" style="width:100%;height:100%;">
            </div>
            
       </td>       
       <td width="50%" height="50%"  style="border:solid;">
            <div id="propBox" width="100%" height="100%" style="width:100%;height:50%;background-color: rgba(255, 255, 0, 0.5);">
                <input type="button" value="Change MEMEBackground" style="width:160;height:40px;" onclick="ChangeBackground();" />
                <input type="button" value="Add Caption" style="width:160;height:40px;" onclick="AddCaption();" />                 
            </div>
           
            <div id="propBox_1" width="100%" height="50%" style="width:100%;height:50%;background-color: rgba(255, 255, 255, 0.5);">
                <input type="text" id="fontsize" value="40" style="width:160;height:40px;" />
                <input type="button" value="Apply" style="width:160;height:40px;" onclick="Apply();" />                 
            </div>
           
       </td>
    </tr>
</table>
</div>
</body>
</html>
"""
class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)

application = webapp2.WSGIApplication([
    ('/meme', MainPage),
], debug=True)