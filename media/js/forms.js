/**
 * DHTML date validation script. Courtesy of SmartWebby.com (http://www.smartwebby.com/dhtml/)
 */
// Declaring valid date character, minimum year and maximum year
var dtCh= "/";
var minYear=1900;
var maxYear=2100;

function IsNumeric(input)
{
   return (input - 0) == input && input.length > 0;
}

function isInteger(s){
	var i;
    for (i = 0; i < s.length; i++){   
        // Check that current character is number.
        var c = s.charAt(i);
        if (((c < "0") || (c > "9"))) return false;
    }
    // All characters are numbers.
    return true;
}

function stripCharsInBag(s, bag){
	var i;
    var returnString = "";
    // Search through string's characters one by one.
    // If character is not in bag, append to returnString.
    for (i = 0; i < s.length; i++){   
        var c = s.charAt(i);
        if (bag.indexOf(c) == -1) returnString += c;
    }
    return returnString;
}

function daysInFebruary (year){
	// February has 29 days in any year evenly divisible by four,
    // EXCEPT for centurial years which are not also divisible by 400.
    return (((year % 4 == 0) && ( (!(year % 100 == 0)) || (year % 400 == 0))) ? 29 : 28 );
}
function DaysArray(n) {
	for (var i = 1; i <= n; i++) {
		this[i] = 31
		if (i==4 || i==6 || i==9 || i==11) {this[i] = 30}
		if (i==2) {this[i] = 29}
   } 
   return this
}

function isDate(dtStr){
	var daysInMonth = DaysArray(12)
	var pos1=dtStr.indexOf(dtCh)
	var pos2=dtStr.indexOf(dtCh,pos1+1)
	var strDay=dtStr.substring(0,pos1)
	var strMonth=dtStr.substring(pos1+1,pos2)
	var strYear=dtStr.substring(pos2+1)
	strYr=strYear
	if (strDay.charAt(0)=="0" && strDay.length>1) strDay=strDay.substring(1)
	if (strMonth.charAt(0)=="0" && strMonth.length>1) strMonth=strMonth.substring(1)
	for (var i = 1; i <= 3; i++) {
		if (strYr.charAt(0)=="0" && strYr.length>1) strYr=strYr.substring(1)
	}
	month=parseInt(strMonth)
	day=parseInt(strDay)
	year=parseInt(strYr)
	if (pos1==-1 || pos2==-1){
		alert("The date format should be : dd/mm/yyyy")
		return false
	}
	if (strMonth.length<1 || month<1 || month>12){
		alert("Please enter a valid month")
		return false
	}
	if (strDay.length<1 || day<1 || day>31 || (month==2 && day>daysInFebruary(year)) || day > daysInMonth[month]){
		alert("Please enter a valid day")
		return false
	}
	if (strYear.length != 4 || year==0 || year<minYear || year>maxYear){
		alert("Please enter a valid 4 digit year between "+minYear+" and "+maxYear)
		return false
	}
	if (dtStr.indexOf(dtCh,pos2+1)!=-1 || isInteger(stripCharsInBag(dtStr, dtCh))==false){
		alert("Please enter a valid date")
		return false
	}
return true
}

function CompDate(adate,bdate)
{
	a = adate.split('/');
	b = bdate.split('/');
	var sDate = new Date(a[2],a[1], a[0]);
	var eDate = new Date(b[2],b[1], b[0]);

	if (sDate > eDate ){
		return false;
	}
}

function validate_search(thisform)
{
	with (thisform)
	{

		/*conesearch empty*/
		var conesearch = 0;
		if (ra.value!=null && ra.value!="") conesearch++;
		if (dec.value!=null && dec.value!="") conesearch++;
		if (size.value!=null && size.value!="") conesearch++;

		if (conesearch>0 && conesearch<3)
		{
			alert('Please, enter all coordinates');
			ra.focus();
			return false;
		}

		/*RA format*/
		if (ra.value!=null && ra.value!="")
		{
			var reRA = new RegExp('^\-?([0-9]{2}):([0-9]{2}):([0-9]{2})\.?([0-9]+)?$');
			var m = reRA.exec(ra.value);

			if (m == null) {
				alert('Please, enter a valid format for RA value');
				ra.focus();
				return false;
			} else {
				if (m[1]>23 || m[2]>59 || m[3]>59)
				{
					alert('RA coordinates must be given in hours');
					ra.focus();
					return false;
				}
			}
		}

		/*DEC format*/
		if (dec.value!=null && dec.value!="")
		{
			var reDEC = new RegExp('^\-?([0-9]{2}):([0-9]{2}):([0-9]{2})\.?([0-9]+)?$');
			var m = reDEC.exec(dec.value);

			if (m == null || m[1]>89) {
				alert('Please, enter a valid format for DEC value');
				dec.focus();
				return false;
			} else {
				if (m[1]>89)
				{
					alert('Please, enter a valid format for DEC value');
					dec.focus();
					return false;
				}
			}
		}

		/*numeric format*/
		if (isNaN(size.value))
		{
			alert('Please, enter a valid number for size value');
			size.focus();
			return false;
		}

		/*size > 30*/
		if (size.value>30)
		{
			alert('Please, enter a size value lower than 30');
			size.focus();
			return false;
		}

		/*source name / position*/
		if (source_name.value!=null && source_name.value!="" && conesearch==3)
		{
			alert('Please, only one field in Source Name / Position block');
			//source_name.value=null;
			//ra.value=null;
			//dec.value=null;
			//size.value=null;
			source_name.focus();
			return false;
		}

		/*numeric format*/
		if (isNaN(opacity.value))
		{
			alert('Please, enter a valid number for opacity');
			size.focus();
			return false;
		}

		/*dates format*/
		if ((date_from.value!=null && date_from.value!="") && isDate(date_from.value)==false){
			alert('Please enter a valid date')
			date_from.focus()
			return false
		}
		if ((date_to.value!=null && date_to.value!="") && isDate(date_to.value)==false){
			alert('Please enter a valid date')
			date_to.focus()
			return false
		}

		/*dates empty*/
		if ((date_from.value!=null && date_from.value!="") && (date_to.value==null || date_to.value==""))
		{
			alert('Please enter Observation Date To')
			date_to.focus()
			return false
		}

		if ((date_to.value!=null && date_to.value!="") && (date_from.value==null || date_from.value==""))
		{
			alert('Please enter Observation Date From')
			date_from.focus()
			return false
		}

		/*dates do not follow*/
		if ((date_to.value!=null && date_to.value!="") && (date_from.value!=null && date_from.value!=""))
		{
			if (CompDate(date_from.value, date_to.value)==false)
			{
				alert('Dates do not follow')
				date_from.focus()
				return false
			}
		}

		/*only batchfile*/
		var f = document.getElementById("id_batchfile");
		if (f.value!=null && f.value!=""){
			return window.confirm('Process only your file data ?');
		}

		/*frequency empty*/
		var frequency = 0;
		if (frequency_from.value!=null && frequency_from.value!="") frequency++;
		if (frequency_to.value!=null && frequency_to.value!="") frequency++;
		if (frequency>0 && frequency<2)
		{
			alert('Please, enter frequency range');
			frequency_from.focus();
			return false;
		}
		if (frequency==2 && int(frequency_from.value)>int(frequency_to.value))
		{
			alert('Frequencies do not follow');
			frequency_from.focus();
			return false;
		}

		/*numeric format*/
		if (isNaN(frequency_from.value))
		{
			alert('Please, enter a valid number for start frequency range');
			frequency_from.focus();
			return false;
		}
		if (isNaN(frequency_to.value))
		{
			alert('Please, enter a valid number for end frequency range');
			frequency_to.focus();
			return false;
		}

		/*velocity empty*/
		var velocity = 0;
		if (velocity_from.value!=null && velocity_from.value!="") velocity++;
		if (velocity_to.value!=null && velocity_to.value!="") velocity++;
		if (velocity>0 && velocity<2)
		{
			alert('Please, enter velocity range');
			velocity_from.focus();
			return false;
		}
		if (velocity==2 && int(velocity_from.value)>int(velocity_to.value))
		{
			alert('Velocities do not follow');
			velocity_from.focus();
			return false;
		}

		/*numeric format*/
		if (isNaN(velocity_from.value))
		{
			alert('Please, enter a valid number for start velocity range');
			velocity_from.focus();
			return false;
		}
		if (isNaN(velocity_to.value))
		{
			alert('Please, enter a valid number for end velocity range');
			velocity_to.focus();
			return false;
		}

		/*frequency / velocity / line name*/
		if (
			(frequency==2  && velocity==2)
			|| (frequency==2  && line_name.value!=null && line_name.value!="")
			|| (velocity==2  && line_name.value!=null && line_name.value!="")
			)
		{
			alert('Please, only one field in Frequency / Velocity / Line Name block');
			//frequency_from.value=null;
			//frequency_to.value=null;
			//velocity_from.value=null;
			//velocity_to.value=null;
			//line_name.value=null;
			frequency_from.focus();
			return false;
		}

		/*global not empty form*/
		if (
			   (source_name.value==null || source_name.value=="")
			&& (ra.value==null || ra.value=="")
			&& (opacity.value==null || opacity.value=="")
			&& (frequency_from.value==null || frequency_from.value=="")
			&& (velocity_from.value==null || velocity_from.value=="")
			&& (line_name.value==null || line_name.value=="")
			&& (date_from.value==null || date_from.value=="")
			&& (project_id.value==null || project_id.value=="")
			&& (batchfile.value==null || batchfile.value=="")
			)
		{

			var checked = false;
			var inputs = document.getElementsByTagName('input');
			var checkboxOptions = [];
			for(var i=0;i<inputs.length;i++){
			  if(inputs.item(i).getAttribute('name') == 'receivers' ){
				checkboxOptions.push( inputs.item(i) );
			  }
			}
            for(var n = 0; n < checkboxOptions.length; ++n)
			if(checkboxOptions[n].checked){checked=true;}
			
			if (checked==false){
				alert('Please, enter some data...')
				return false;
			}
		}
	}

	return true;

}
