src = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"
const search_input = document.getElementById('search')
const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value
const results_box = document.getElementById('results-box')

const new_url = '/news/'

const send_search_data = (search_text) => {
    $.ajax({
        url: '/search_api',
        type: 'POST',
        data: {
            search_text: search_text,
            csrfmiddlewaretoken: csrf_token,
        },
        success: function (result) {
            console.log('yeah')
            console.log(result.data)
            results_box.style.visibility = 'visible';
            const data = result.data
            if (Array.isArray(data)) {
                results_box.innerHTML = ""
                data.forEach(i => {
                    results_box.innerHTML += `
                            <a href='${new_url}${i.id}' class="how-txt1 size-a-6 f1-s-8  cl1 hov-cl10 trans-03">
                            <div class="row mt-2 mb-2">
                            <div class="col-2">
                            <img src="${i.img}" class="results-img">
                            </div>
                            <div class="col-10">
                            <h5>${i.name}</h5>
                            <p class="text-muted">${i.date}</p>
                            </div>
                            </div>
                            
                            </a>
                            `
                })
            } else {
                if (search_input.value.length > 0) {
                    results_box.innerHTML = `<b class="how-txt1 size-a-6 f1-s-8  cl1 hov-cl10 trans-03">${data}</b>`
                } else {
                    results_box.innerHTML = ''
                    results_box.style.visibility = 'hidden';
                }

                console.log('not array')
            }
            // if (result != 'No task_id in the request'){
            //     document.getElementById('progress-block').style.visibility = 'visible' ;
            //    }
            //
            // if (result == "SUCCESS") {
            //     document.getElementById('task_id').value = task_id ;
            //     document.getElementById('task_id2').value = task_id ;
            //     document.getElementById('returnBtn').style.visibility = 'visible';
            //     document.getElementById('download_uri').style.visibility = 'visible';
            //
            //     document.getElementById('task_id').value = task_id ;
            //
            //     willstop = 1;
            //
            //    }
        },
        error: (err) => {
            console.log('fail')
            console.log(err)
        }
    });
};

// var refreshIntervalId = setInterval(function() {
//   poll();
//   if(willstop == 1){
//     clearInterval(refreshIntervalId);
//   }
// },500);


// })();


search_input.addEventListener('keyup', e => {
    console.log(e.target.value)
    send_search_data(e.target.value)
})
