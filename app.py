<!DOCTYPE html>
<html>
<head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
    <script>
        $(document).ready(function(){
            $(".hide").hide();
            $(':radio').change(function(){
                var isChecked = $(this).prop('checked');
                var isShow = $(this).hasClass('hide_class');
                
                $(".cidr_class").toggle(isChecked && isShow);
                $("#subnet_id").toggle(isChecked && !isShow);
                
                if($(this).val()==1)
                    {
                        $("#cidr").val('');
                        $("#mask").prop("required", true);
                    }
                else 
                    if($(this).val()=="2")
                    {
                        $("#mask").val('');
                        $("#cidr").prop("required", true);
                    }
                });

            $( "#submit" ).click(function() {
                var ip_val=$("#ip").val();
                var ip_split= ip_val.split(".");

                if(ip_split.length!=4)
                {
                    alert("wrong ip format" );
                    return false;
                }
                for(var i=0;i<4;i++)
                {
                    if($.isNumeric(ip_split[i])&&ip_split[i]>=0&&ip_split[i]<=255)
                        continue;
                    else
                    {
                        alert("wrong Ip format");
                        return false;
                    }
                }
                if ( $( "#choice:checked").val() == "2" )
                {
                    var cidr_val= $( "#cidr").val();
                    if ( cidr_val < 32 && /^\d+$/.test(cidr_val));
                    else
                    {
                        alert("wrong CIDR format");
                        return false;
                    }
                }
                if ( $( "#choice:checked").val() == "1" )
                {
                    var mask_val=$("#mask").val();
                    if((mask_val.match(/\./g)).length!=3)
                    {
                        alert("wrong mask");
                        return false;
                    }
                    var mask_split= mask_val.split(".");
                    var se1=0;var binary="";var final_bin="";
                    for (var i=0;i<=3;i++)
                      {
                       var pos=0;
                       mask_group=mask_split[i];
                       while(mask_group>0)
                        { 
                            pos++;
                            binary=(mask_group%2)+""+binary;
                            mask_group=parseInt(mask_group/2);
                        }
                        while(pos<=7)
                        {
                            binary="0"+binary;
                            pos++;
                        }
                          final_bin+= binary;
                          binary="";
                      } //end of for 
                    binary= final_bin;
                
                //to check if first occurenxt of 1 is not at the first position    
                if(binary.indexOf("1")>0)
                  {
                      alert("wrong mask format");
                      return false;
                  }
                    
                  //check if 1 is presnt in the mask
                   if(binary.indexOf("1")==0)
                     {
                      se1=1;  //check for 1 after the 0th position
                      var set0=binary.indexOf("0");

                      if(binary.indexOf("1",se1)!=-1)
                       {
                         alert("wrong mask format");
                           return false;
                       }
                      }
                    }
                 
               $.ajax({
            url: '/prob1_solution',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
               $("#output").html(response);
            },
            error: function(error) {
                $("#output").html(error);
            }
            });
        });
    });
    </script>
</head>
<body>

<form id="myForm" method="POST" action="http://localhost:5000/prob1_solution">
    <fieldset>
        <legend>Problem 1:</legend>
        <table style="text-align:center; margin-left:25%">
            <tr>
                <td>IP Address:</td>
                <td><input type="text" name="ip" id="ip" title="Enter valid IP address" placeholder="XXX.XXX.XXX.XXX" required></td>
            </tr>
            <tr>
                <td> Subnet mast  <input type ="radio" name="choice" id="choice" value="1" checked></td>
                <td> CIDR  <input type ="radio" name="choice" class="hide_class" id="choice" value="2"></td>
            </tr>

            <tr id="subnet_id">
                <td>Subnet Mask:</td>
                <td><input type="text" name="mask" id="mask" title="Enter valid subnet mask" placeholder="XXX.XXX.XXX.XXX"required></td>
            </tr>

            <tr class="cidr_class" style="display:none">
                <td></td>
                <td>/</td>
            </tr>

            <tr class="cidr_class" style="display:none">
                <td>CIDR:</td>
                <td><input type="text" name="cidr" id="cidr" ></td>
            </tr>
        </table>
        <input type="submit" value="Submit" id="submit" style="text-align:center">
    </fieldset>
</form>
<div id="output"></div>
</body>
</html>