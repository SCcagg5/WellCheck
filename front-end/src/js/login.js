new Vue(
  {
    el: '#login',
    data: {
    password: "",
    mail: "",
    error: ""
    },
  methods:{
    log: function() {
       this.ajaxRequest = true;
       data = {
          "mail" : this.mail,
          "password": this.password
        };
       url = "http://51.75.30.103/connect/"
       axios.post(url, data)
            .then(response => {this.checklog(response.data)})
            .catch(error => console.log(error));
     },
     checklog: function(resp) {
       console.log(resp)
       if(!resp.succes){
         this.error = '<div class="alert alert-danger alert-dismissible" role="alert" ><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button><i class="fa fa-times-circle"></i> Informations invalides</div>'
       }else{
         localStorage.mail = resp.data.mail;
         localStorage.token = resp.data.token;
           window.location.href = "index.html";
       }
     },
 },
 mounted(){
    if (localStorage.mail && localStorage.token) {
      window.location.href = "index.html";
    }
 }
})
