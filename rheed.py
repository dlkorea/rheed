import numpy as np
import cv2
import matplotlib.pyplot as plt
from operator import add


def main():
    filename = input('동영상 파일명을 입력하세요. : ')
    cap = cv2.VideoCapture(filename)
    print_video_info(cap)
    x_range, y_range = input_area(cap)
    data = get_avg_list(cap, x_range, y_range)    
    plot(data)
    save_on_file(data)


def print_video_info(video_capture):
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print('width: {0}, height: {1}, fps: {2}'.format(width, height, fps))


def input_two_int(input_str):
    while True:
        raw_input = input(input_str)
        try:
            x, y = raw_input.split(',')
            point = (int(x), int(y))
            break
        except ValueError:
            print('입력한 형식에 문제가 있습니다.')
    return point


def input_area(video_capture):
    while True:
        anchor_point = input_two_int('기준점을 x,y로 입력하세요. ex)1,2 : ')
        size = input_two_int('원하는 width, height 를 입력하세요.\n기준점으로부터 우측 하단으로 지정됩니다. ex) 100,100 : ')
        opposite_point = tuple(anchor_point[i] + size[i] for i in range(len(anchor_point)))

        video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        copied_frame = video_capture.read()[1].copy()
        if confirm_area(copied_frame, anchor_point, opposite_point):
            break
    x_range = (anchor_point[0], opposite_point[0])
    y_range = (anchor_point[1], opposite_point[1])

    return (x_range, y_range)


def confirm_area(frame, anchor_point, opposite_point):
    cv2.rectangle(frame, anchor_point, opposite_point, (255, 255, 255), 1)
    cv2.imshow('Selected Area', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    while True:
        answer = input('이 영역이 맞습니까? (Y/n) : ')
        if answer in ['y','n', '']:
            break
        else:
            print('Y, y, N, n, 엔터(예스로 인식) 중에 입력하세요.')

    return answer in ('y', '')


def get_avg_list(cap, x_range, y_range):
    avg_list = []
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        avg = frame[y_range[0]:y_range[1], x_range[0]:x_range[1]].mean()
        avg_list.append(avg)
    return avg_list


def plot(data):
    plt.plot(data)
    plt.xlabel('Frame of Video')
    plt.ylabel('Average Intensity')
    plt.show()


def save_on_file(data):
    filename = input('저장할 파일명을 입력하세요.(확장자 x)(기존 파일명과 중복되면 덮어씁니다.) : ') + '.txt'
    with open(filename, 'w') as f:
        for frame_count, avg_intensity in enumerate(data):
            f.write('{0} {1}\n'.format(frame_count, avg_intensity))
    print('{0}에 저장하였습니다.'.format(filename))


if __name__ == '__main__':
    main()
