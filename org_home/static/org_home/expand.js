function addExpandButton(id,name)
{
    subCategories = subCategoriesAndId(name);
    if (subCategoriesAndId(name)[0].length != 0)
    {
        document.getElementById(id).innerHTML += "<button class='expandButton' id=\"exp" + id + "\" onclick=\"expand('" + id + "', '" + name + "')\">></button></div>";
    }
}
function subCategoriesAndId(parent_name)
{
    var subCategoryList = [];
    var subCategoryIdList = [];
    {% for category in categories_list %}
        if ("{{ category.parent }}" == parent_name)
        {
            var c = "{{ category.category_name }}";
            var id = "{{ category.id }}";
            subCategoryList.push(c);
            subCategoryIdList.push(id);
        }
    {% endfor %}
    return [subCategoryList,subCategoryIdList]
}
<!--Will expand to show the list of subcategories-->
function expand(divName,parent_name){
    subCategories = subCategoriesAndId(parent_name);
    var subCategoryList = subCategories[0];
    var subCategoryIdList = subCategories[1];
    var newdiv = document.createElement('div');
    newdiv.id = "close" + divName;
    var checkOnPage =  document.getElementById(newdiv.id);
    if (checkOnPage == null){
        for (c in subCategoryList){
            id = subCategoryIdList[c];
            var name = subCategoryList[c];
            url = "{% url 'org_home:individualCategory' organization_id=organization.id category_id=123 %}".replace("123", subCategoryIdList[c]);
            if (subCategoriesAndId(name)[0].length != 0){
                newdiv.innerHTML += "<div style='margin-left:15px' id=" + id + ">\
                <a style='margin-left: 20px; text-decoration:none' href = " +  url + " >" + name + "</a>\
                <button class='expandButton' id=\"exp" + id + "\" onclick=\"expand('" + id + "', '" + name + "')\">></button></div>";
            }
            else{
                newdiv.innerHTML += "<div style='margin-left:15px' id=" + id + ">\
                <a style='margin-left: 20px; text-decoration:none' href = " +  url + " >" + name + "</a>";
            }

        }
        document.getElementById(divName).innerHTML += "<input class='expandButton' id='closeButton" + divName + "' type=button value='v' onclick=\"contract('" + divName + "')\"/>";
        document.getElementById(divName).appendChild(newdiv);
        document.getElementById("exp" + divName).style.display='none';
        }
    }
function contract(divName){
    document.getElementById("close" + divName).remove();
    document.getElementById("closeButton" + divName).remove();
    document.getElementById("exp" + divName).style.display = '';
    }
