"use strict";(self["webpackChunkarchivechat"]=self["webpackChunkarchivechat"]||[]).push([[443],{5710:function(t,e,s){s.r(e),s.d(e,{default:function(){return T}});var i=function(){var t=this,e=t._self._c;return e("div",{staticClass:"outbox"},[e("div",{staticClass:"main"},[e("div",{staticClass:"friendList"},[t._l(t.friendList,(function(s){return e("Friend_Item",{key:s.id,attrs:{chosen:t.displayDialog==s.name,id:s.id,name:s.name,group:!1},on:{switchDialog:t.switchDialog}})})),t._l(t.groupList,(function(s){return e("Friend_Item",{key:s.id,attrs:{chosen:t.displayDialog==s.name,id:s.id,name:s.name,group:!0},on:{switchDialog:t.switchDialog}})}))],2),e("div",{staticClass:"chatBox",style:{translate:t.showChatBox?"15%":"120%"}},[e("button",{staticClass:"goback",staticStyle:{"background-color":"azure","border-left":"5px yellow solid",height:"5%",width:"10%",position:"absolute",left:"-2%","transition-duration":"0.4s","font-weight":"bold"},style:{top:t.showChatBox?"5%":"90%"},on:{click:function(e){t.showChatBox=!t.showChatBox}}},[e("p",{staticStyle:{transform:"skew(20deg)"}},[t._v(t._s(this.showChatBox?"返回":"展开"))])]),e("button",{staticStyle:{"background-color":"azure","border-right":"5px aqua solid",height:"5%",width:"10%",position:"absolute",right:"-2%","transition-duration":"0.4s",bottom:"2%","font-weight":"bold"},on:{click:t.sendMsg}},[e("p",{staticStyle:{transform:"skew(20deg)"}},[t._v("发送")])]),e("button",{staticStyle:{"background-color":"azure","border-right":"5px aqua solid",height:"5%",width:"10%",position:"absolute",right:"-2%","transition-duration":"0.4s",bottom:"10%","font-weight":"bold"},on:{click:function(e){t.showfilebox=!t.showfilebox}}},[e("p",{staticStyle:{transform:"skew(20deg)"}},[t._v("文件")])]),e("div",{staticClass:"msgBox"},t._l(t.currentMsgList,(function(s){return e("MsgBubble",{key:s.timestamp,staticStyle:{transform:"skew(20deg)"},attrs:{myself:s.userId==t.userId,speaker:s.userId,msg:s.msg,filename:s.fileName,type:s.type,progress:s.progress},on:{downloadHandler:t.downloadHandler}})})),1),e("div",{staticClass:"inputBox"},[e("textarea",{directives:[{name:"model",rawName:"v-model",value:t.inputmsg,expression:"inputmsg"}],attrs:{placeholder:"这里是聊天框",required:"",maxlength:"240"},domProps:{value:t.inputmsg},on:{input:function(e){e.target.composing||(t.inputmsg=e.target.value)}}})])])]),e("fileSendingCard",{style:{translate:t.showfilebox?"0":"-500%"},on:{closeFileBox:t.closeFileBox,sendFileHandler:t.sendFileHaDiadisplayChatBoxndler}})],1)},a=[],o=(s(7658),function(){var t=this,e=t._self._c;return e("div",{class:{itembox:!t.chosen,chosenItem:t.chosen},on:{click:t.clickhandler}},[e("div",{staticClass:"icon"}),e("div",[e("ul",{staticClass:"content"},[e("li",{staticClass:"text"},[e("span",[t._v(t._s(1==this.group?"(群)":" ")+t._s(this.name))])]),e("li",[t._v(t._s(this.id))])])])])}),n=[],l={props:{id:{type:String},name:{type:String},group:{type:Boolean},chosen:{type:Boolean}},methods:{clickhandler(){let t={id:this.id,name:this.name,group:this.group};this.$emit("switchDialog",t)}}},r=l,d=s(1001),c=(0,d.Z)(r,o,n,!1,null,"265f5c70",null),u=c.exports,h=function(){var t=this,e=t._self._c;return e("div",{class:{outBox:!0,"align-left":!t.myself,"align-right":t.myself}},[e("div",{class:{speaker:!t.myself,myself:t.myself}},[t._v(t._s(this.speaker))]),e("div",{staticClass:"msgBox"},[t._v(t._s(this.msg)+t._s(this.filename)),"file"==this.type&&0==this.myself?e("span",{staticStyle:{color:"green",cursor:"pointer"},on:{click:t.download}},[t._v(" "+t._s(this.downloading?"停止":"下载"))]):t._e()]),"file"==this.type&&0==this.myself?e("ProgressBar",{attrs:{progress:t.progress}}):t._e()],1)},p=[],g=function(){var t=this,e=t._self._c;return e("div",{staticClass:"progress-bar"},[e("div",{staticClass:"progress",style:{width:t.progress+"%"}})])},m=[],f={props:{progress:{type:Number}}},y=f,w=(0,d.Z)(y,g,m,!1,null,null,null),x=w.exports,v={props:{type:{type:String},speaker:{type:String},myself:{Type:Boolean},msg:{type:String},progress:{type:Number},filename:{type:String}},data(){return{downloading:!1}},methods:{download(){this.downloading=!this.downloading,this.$emit("downloadHandler",this.filename)}},components:{ProgressBar:x}},b=v,_=(0,d.Z)(b,h,p,!1,null,"5699099e",null),C=_.exports,B=s(6154),L=function(){var t=this,e=t._self._c;return e("div",{staticClass:"box"},[e("button",{staticClass:"goback",staticStyle:{"background-color":"azure",padding:"10px 20px 10px 20px","border-left":"5px yellow solid",position:"absolute",left:"-2%","transition-duration":"0.4s","font-weight":"bold",top:"5%"},on:{click:t.closeFileBox}},[e("p",{staticStyle:{transform:"skew(20deg)"}},[t._v("关闭")])]),e("p",{staticClass:"title"},[t._v(" ENTER FILE PATH")]),e("input",{directives:[{name:"model",rawName:"v-model",value:t.path,expression:"path"}],staticClass:"filepathinput",domProps:{value:t.path},on:{input:function(e){e.target.composing||(t.path=e.target.value)}}}),e("button",{staticClass:"submit",on:{click:t.sendfiletrigger}},[t._v("发送")])])},k=[],I={data(){return{path:""}},methods:{sendfiletrigger(){if(""==this.path)return void alert("NO EMPTY PATH");let t=this.path.split("/").join("//");this.$emit("sendFileHandler",t)},closeFileBox(){this.$emit("closeFileBox")}}},N=I,S=(0,d.Z)(N,L,k,!1,null,"2b4803ca",null),D=S.exports,F={mounted(){window.AboutView=this;let t=this;t.userId=window.localStorage.getItem("username"),t.username=window.localStorage.getItem("username"),"Alice"==t.username&&t.friendList.push({id:"Bob",name:"Bob",msgList:[]}),"Bob"==t.username&&t.friendList.push({id:"Alice",name:"Alice",msgList:[]}),console.log(t.username),this.fetchMsgList(),this.timer=window.setInterval((()=>{setTimeout((()=>{this.fetchMsgList()}),0)}),5e3)},methods:{async fetchMsgList(){let t=await B.Z.post("/api/fetch_msg_list");console.log(t.data.msg),this.updateMsgListBuffer(t.data.msg)},updateMsgListBuffer(t){t.forEach((e=>{try{let s;"private"==e.source?s=this.friendList.find((t=>t.id==e.userId||t.id==e.target)):"group"==e.source&&(s=this.groupList.find((t=>t.id==e.userId||t.id==e.target))),console.log(t),console.log(s),s.msgList.push(e)}catch(s){console.warn(s)}this.refreshChatBox(this.displayDialog)}))},sendMsg(){if(""==this.inputmsg)return alert("empty inputbox"),0;{let e={type:"text",target:this.displayDialog,msg:this.inputmsg};console.log(e);try{B.Z.request({data:e,method:"post",url:"group"!=this.displayType?"/api/send_msg":"/api/send_group_msg"}),this.inputmsg=""}catch(t){console.log(t)}}},switchDialog(t){console.log("switch to"+t.name),this.displayType=1==t.group?"group":"private",this.displayDialog=t.name,this.refreshChatBox(t.name),this.showChatBox=!0},addChatHandler(t){t.chatName!=this.username?(0==t.ifGroup?this.friendList.push({id:t.chatName,name:t.chatName,msgList:[]}):this.groupList.push({id:t.chatName,name:t.chatName,msgList:[]}),this.switchDialog({id:t.chatName,name:t.chatName,group:t.isGroup})):alert("INVALID CHATNAME")},refreshChatBox(t){this.currentMsgList.splice(0,this.currentMsgList.length);try{let e=this.friendList.find((e=>e.name==t))||this.groupList.find((e=>e.name==t));e.msgList.forEach((t=>{this.currentMsgList.push(t)}))}catch(e){console.log(e)}},triggerFileInput(){document.getElementById("file").click()},onFilepathChange(t){let e=t.target.files[0];if(console.log(e),window.FileReader){let t=new FileReader;t.readAsDataURL(e),t.onloadend=function(t){this.filepath=t.target.result,this.filepath=t.target.result,window.localStorage.setItem("filepath",t.target.result),console.log(localStorage.getItem("filepath"))}}},async sendFileHandler(t){if(""==this.displayDialog)return void alert("NO CHOSEN TARGET");let e={target:this.displayDialog,filePath:t};try{await B.Z.request({method:"post",data:e,url:"/api/send_file"})}catch(s){console.log(s)}this.showfilebox=!1},async downloadHandler(t){""!=this.displayDialog?B.Z.request({method:"post",data:{target:this.displayDialog,fileName:t,op:"start"},url:"/api/file_op"}):alert("EMPTY SENDING TARGET")},closeFileBox(){this.showfilebox=!1}},data(){return{username:"Zhier123",userId:"Zhier123",displayDialog:"",displayType:"",inputmsg:"",filepath:null,showfilebox:!1,showChatBox:!1,friendList:[{name:"Ordinary",id:"偶像宅",msgList:[{userId:"Zhier123",target:"Ordinary",type:"text",msg:"hello"},{userId:"Ordinary",target:"Zhier123",type:"text",msg:"妈妈生的"}]},{name:"平克顿二号",id:"现充",msgList:[]},{name:"Link",id:"don't buy lite",msgList:[]}],groupList:[{name:"粉红5人",id:"平克顿侦探事务所",msgList:[]}],currentMsgList:[]}},destroyed(){window.clearInterval(this.timer)},components:{Friend_Item:u,MsgBubble:C,fileSendingCard:D}},M=F,E=(0,d.Z)(M,i,a,!1,null,"3a7b23ff",null),T=E.exports},4338:function(t,e,s){s.r(e),s.d(e,{default:function(){return d}});var i=function(){var t=this,e=t._self._c;return e("div",{staticClass:"about"},[e("h1",[t._v("This is an about page")]),e("div",{staticClass:"inputfile"},[e("button",{attrs:{type:"primary"},on:{click:function(e){return t.openFile()}}},[t._v("选择文件")]),e("input",{directives:[{name:"model",rawName:"v-model",value:t.textarea,expression:"textarea"}],attrs:{id:"textbox",placeholder:"open file"},domProps:{value:t.textarea},on:{input:function(e){e.target.composing||(t.textarea=e.target.value)}}}),e("input",{staticStyle:{display:"none"},attrs:{type:"file",name:"filename",id:"open"},on:{change:function(e){return t.specifiName(e)},input:function(e){return t.specifiName(e)}}})])])},a=[],o={data(){return{textarea:""}},methods:{openFile(){document.getElementById("open").click()},specifiName(t){console.log(t),document.getElementById("textbox").value=document.getElementById("open").files[0].path}}},n=o,l=s(1001),r=(0,l.Z)(n,i,a,!1,null,null,null),d=r.exports}}]);
//# sourceMappingURL=about.45ea7b1c.js.map