input_video=$1
start_time=$2
duration=$3

ffmpeg -ss $2 -i $1 -t $3 -y -c:v copy -c:a copy ./new_queries/output_video.mp4 -t $3 ./new_queries/output_video.wav &> /dev/null

time python Code/main.py ./new_queries/output_video.mp4 ./new_queries/output_video.wav