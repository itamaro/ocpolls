 $(function() {
	 
	var sortObj = {
		      connectWith: "ul",
		      axis: "y",
		      handle: ".grab",
		      dropOnEmpty: true,
		      receive:function(e,ui){
		    	  var $this = $(this);
		    	  handleDrop();
		    	  
		    	  function handleDrop(){
			    	  if ($this.hasClass("dropAble")){
			    		  addNewList($this,ui.item);
			    	  }
			    	  //if has no li's - kill ul
			    	  if(ui.sender.find("li").length == 0){
			    		  ui.sender.next().remove(); //using next! so be sure not to put DOM element between ul's
			    		  ui.sender.remove();
			    	  }
		    	  }
		    	  
		    	  function addNewList($list,$item){
		    		  //create new list
		    		  $newList = $("<ul>").addClass("dropList");
		    		  //add new list to page and add the dropped item into it
		    		  $list.after($newList.sortable(sortObj).append($item));
		    		  //if dropped into 'dropAble' list - add new 'dropAble' list below
		    		  if ($list.hasClass("dropAble")){
		    			  $newList.after($("<ul>").addClass("dropList dropAble").sortable(sortObj));
		    		  }
		    	  }
		      }
		    }; 
	 
	 
	
	init();
	
	function fillPoll(){
		
		$.each(data,function(i,val){
			
			$("<li>")
			.attr({
				id:i
			})
			.addClass("ui-state-default")
			.append('<div class="grab"></div>' + val)
			.appendTo($("#listDefault"));
			
			
			
		});
		
	}
	
	function init(){
		// initialize main list 
		var $theList = $("ul.dropList").sortable(sortObj);
		fillPoll();
		// add drop list below and above
		$theList.before($("<ul>").addClass("dropList dropAble").sortable(sortObj));
		$theList.after($("<ul>").addClass("dropList dropAble").sortable(sortObj));
		
		$(".dropList").disableSelection();
		
		
		
		// bind click to submit button
		$("#btnSubmit").click(function(){
			var arr = new Array();
			
			//build array to send
			$("ul.dropList").each(function(i,list){
				if ($(list).find("li").length){
					var innerArray = new Array();
					$(list).find("li").each(function(i,item){
						innerArray.push($(item).attr("id"));
					});
					arr.push(innerArray);
				}
			});
			
			//TODO: send array to server side
			$("#hiddenVote").val(arrayToString(arr));
			console.log(arrayToString(arr));
			console.log(arr);
		});
	}
	
	function arrayToString(arr){
		var str = "[";
		for(var i=0; i<arr.length;i++){
			var strInner = "[";
			strInner += arr[i].toString();
			strInner += "]";
			
			if (i != arr.length-1){
				strInner+=",";
			}
			
			str += strInner;
		}
		str +=	"]";
		return str;
	}
	
	
});