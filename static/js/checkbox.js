var require;

function required()
{
  var flag = 0;
      if(document.getElementById("male").checked || document.getElementById("female").checked || document.getElementById("other").checked)
      {
        flag++;
      }

      if(
        document.getElementById("checkboxzero").checked || document.getElementById("checkboxOne").checked ||
        document.getElementById("checkboxTwo").checked || document.getElementById("checkboxThree").checked ||
        document.getElementById("checkboxFour").checked || document.getElementById("checkboxFive").checked ||
        document.getElementById("checkboxSix").checked || document.getElementById("checkboxSeven").checked ||
        document.getElementById("checkboxEight").checked || document.getElementById("checkboxNine").checked ||
        document.getElementById("checkboxTen").checked || document.getElementById("checkboxEleven").checked ||
        document.getElementById("checkboxTwelve").checked || document.getElementById("checkboxThirteen").checked ||
        document.getElementById("checkboxFourteen").checked || document.getElementById("checkboxFifteen").checked     
      )
      {
        flag++;
      }

      if(document.getElementById("checkboxyes").checked || document.getElementById("checkboxno").checked)
      {
        flag++;
      }
    
  
  if(flag < 3)
  {
    console.log(flag);
    alert("Please check all required fields.")
  }
  else
  {
    console.log("LOOKING GOOD");
    return true;
  }
}

function gender(j)
          {
            var total=0;
            for(var i=0; i < document.form1.MorF.length; i++)
            {
              if(document.form1.MorF[i].checked)
              {
                total =total +1;
              }
              if(total > 1)
              {
                alert("Please choose only one gender") 
                document.form1.MorF[j].checked = false ;
                return false;
              }
            }
          }

          function symptoms(i)
          {
            if(i != 0 && document.form1.symptom[0].checked)
            {
              alert("Please deselect 'No Symptoms' to choose other symptoms")
              document.form1.symptom[i].checked = false ;
                return false;
            }
            if(i == 0 && document.form1.symptom[0].checked)
            {
                for(j = 1; j < document.form1.symptom.length; j++)
                {
                    document.form1.symptom[j].checked = false ;

                }
            }

          }

          function vaccines(j)
          {
            if(j == 1 && document.form1.vaccine[0].checked)
            {
              document.form1.vaccine[0].checked = false ;

              document.form1.vaccine[1].checked = true ;
                return true;
            }

            else if(j == 0 && document.form1.vaccine[1].checked)
            {
              document.form1.vaccine[1].checked = false;

              document.form1.vaccine[0].checked = true ;
                return true;
            }
          }

          function covidTests(i)
          {
            if(i == 1 && document.form1.covidTest[0].checked)
            {
              document.form1.covidTest[0].checked = false ;

              document.form1.covidTest[1].checked = true ;
                return true;
            }

            else if(i == 0 && document.form1.covidTest[1].checked)
            {
              document.form1.covidTest[1].checked = false;

              document.form1.covidTest[0].checked = true ;
                return true;
            }

          }
          // function formcheck() {
          //   var fields = $(".ss-item-required")
          //         .find("select, textarea, input").serializeArray();
          
          //   $.each(fields, function(i, field) {
          //     if (!field.value)
          //       alert(field.name + ' is required')
          //    });
          //   console.log(fields);
          // }