$(document).ready( function(){
    var username = 'gazal'
    var password = 'qwerty123'
    var api_url = "/api/"
    var auth_token = 'Bearer ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc5NTA5Mzk2LCJqdGkiOiI4Nzk3Y2M4NzE1NDc0ZGRjOGFjNTk3NzcyZDIyZjNiYSIsInVzZXJfaWQiOjF9.Ua1mbT9dHJH0Vanloo-_mb0jlYpsJ3UM0dn_mSzGvKc'

    $.ajax({
        url: api_url + 'user_stores',
        contentType: "application/json",
        headers: {
            'Authorization': auth_token
        },
        method: 'GET',
        success: function(result){
            console.log(result);
            stores_table_str = ``
            result.forEach(function(elem, index){
                stores_table_str = stores_table_str + `<tr>
                    <th scope="row">${elem.name}</th>
                    <td>${elem.city}</td><td>`
                elem.items.forEach(function(item, index){
                    item_name = item.name;
                    item_price = item.price
                    stores_table_str = stores_table_str + `${item_name} (${item_price})<br/>`
                })
                stores_table_str = stores_table_str + `</td><td>${elem.followed_by.length}</td></tr>`
            });
            $("#store_table").html(stores_table_str)
        }
    })
});