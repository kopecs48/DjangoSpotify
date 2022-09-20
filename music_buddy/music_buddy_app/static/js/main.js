/*
    For any functionality that shouldn't render a new page goes here
*/

$(document).ready(function(){
    
    // Add a song to the Liked Songs Playlist
    $(".like").click(function(){
        $.ajax({
            url:'add_liked_song/',
            type: 'get',
            data: {
                song_id: $(this).attr('value'),
            },
            success: function(response) {
                alert("Song added to Likes"); // Probably gonna change this
            },
            error: function(response){
                alert(response['responseJSON']['error']);
             }
        });
    });

    /* TODO: Add other function for Dislike (and Save)*/
    // Dislike song functionality
    $(".dislike").click(function(){
        $.ajax({
            url:'add_disliked_song/',  // Need to adjust this
            type: 'get',
            data: {
                song_id: $(this).attr('value'),
            },
            success: function(response) {
                alert("Song added to Dislike"); // Probably gonna change this
            }
        });
    });

    /*  Deal with later or something
    $(".send").click(function(){
        $.ajax({
            url:'send_friend_request/',  // Need to adjust this
            type: 'get',
            data: {
                userID: $(this).val(),
            },
            success: function(response) {
                window.location.href = window.location.href;
            }
        });
    });
    */
});