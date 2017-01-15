curl -X DELETE -H "Content-Type: application/json" -d '{
  "setting_type":"greeting"
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=<fb_page_access_token>"

curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type":"greeting",
  "greeting":{
    "text":"Hi {{user_first_name}}! Hugs from KitabiKeeda. I am going to be your personal assistant to help you browse through the books in KGP Central Library. Just tap Get Started below."
  }
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=<fb_page_access_token>"
