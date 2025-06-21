let graph;
const now = new Date();
const day = now.getDate();
const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const currentMonth = month[now.getMonth()];
document.getElementById(currentMonth).selected = "true";
        
function MinToHour(Tmin){
    let Time_Hours = Tmin/60
    let Time_Min = Tmin%60
    if (Math.floor(Time_Hours) == 0){
        return Time_Min
    }else{
        var ReturnValue = Math.floor(Time_Hours) + "h and " + Time_Min
        return ReturnValue
    
    }
}
            
function CreateChart(labels, dados) {
    const ctx = document.getElementById('graph').getContext('2d');

    if (graph) {
        graph.destroy();
    }

    graph = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Screen time',
                data: dados,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#ffffff'
                    },
                    grid: {
                        color: '#333333'
                    }
                    },
                        x: {
                            ticks: {
                                color: '#ffffff'
                            },
                            grid: {
                                color: '#333333'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: '#ffffff'
                            }
                        },
                        tooltip: {
                            enabled: true,
                            callbacks: {
                                label: function(context) {
                                    const min = context.raw;
                                    return MinToHour(min) + " min";
                        }
                    }
                }
            }
        }
    })
}

function LoadData() {
            const mes = document.getElementById('mes').value;

            fetch(`/dados?mes=${mes}`)
                .then(response => response.json())
                .then(data => {
                    const labels = data.map(item => `Dia ${item.dia}`);
                    const val = data.map(item => item.tempo);
                    
                    CreateChart(labels, val);

                    if (data.length > 0) {
                        const max = Math.max(...val);
                        const min = Math.min(...val);
                        const total = val.reduce((a, b) => a + b, 0);
                        const Average = Math.round(total / val.length);

                        const currentDay = data.find(item => item.dia == day).tempo
                        const DayMoreUse = data.find(item => item.tempo === max).dia;
                        const DayLessUse = data.find(item => item.tempo === min).dia;

                        console.log(currentDay)

                        document.getElementById('currentDay').textContent = MinToHour(currentDay);
                        document.getElementById('DaymoreUse').textContent = `Day ${DayMoreUse} (${MinToHour(max)} min)`;
                        document.getElementById('DayLessUse').textContent = `Day ${DayLessUse} (${MinToHour(min)} min)`;
                        document.getElementById('MonthTotal').textContent = MinToHour(total);
                        document.getElementById('DayAverage').textContent = MinToHour(Average);
                        
                    }
                });
            
        }

// Carregar ao iniciar
window.onload = LoadData();