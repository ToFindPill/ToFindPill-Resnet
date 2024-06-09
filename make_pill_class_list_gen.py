import os
import random
from utils import save_dict_to_json, read_dict_from_json
from pathlib import Path
from get_cli_args import get_cli_args  # 설정을 가져오는 함수를 불러옵니다.

def make_pill_class_list():
    args = get_cli_args()  # 설정 로드

    pill_class0 = []
    pill_class1 = []
    sharpness_data = read_dict_from_json(args.json_pill_label_path_sharp_score)
    
    if sharpness_data is None:
        print("Sharpness data could not be loaded. Please check the file path and format.")
        return  # 함수 실행 중단

    pill_sharpness_scores = sharpness_data['pill_label_path_sharp_score']

    # 각 이미지 파일을 클래스별로 분류합니다.
    for entry in pill_sharpness_scores:
        label, pillid, score_mean, score_min, score_max = entry

        # 이미지 파일 경로 설정
        pill_image_path = Path(args.dir_pill_class_base) / pillid

        # 이미지 파일 경로 검사
        if not pill_image_path.exists():
            continue

        for image_file in pill_image_path.glob('*.png'):
            if int(image_file.stem.split('_')[-3]) in args.pill_dataset_class0:
                pill_class0.append(str(image_file))
            elif int(image_file.stem.split('_')[-3]) in args.pill_dataset_class1:
                pill_class1.append(str(image_file))

    # 데이터 분할 함수
    def split_data(data):
        random.shuffle(data)
        n_train = int(len(data) * args.pill_dataset_train_rate)
        n_valid = int(len(data) * args.pill_dataset_valid_rate)

        train_data = data[:n_train]
        valid_data = data[n_train:n_train + n_valid]
        test_data = data[n_train + n_valid:]

        return train_data, valid_data, test_data

    # 클래스별로 데이터 분할
    class0_train, class0_valid, class0_test = split_data(pill_class0)
    class1_train, class1_valid, class1_test = split_data(pill_class1)

    # 결과 딕셔너리 구성
    result_dict = {
        "pngfile_class0_train": class0_train,
        "pngfile_class0_valid": class0_valid,
        "pngfile_class0_test": class0_test,
        "pngfile_class1_train": class1_train,
        "pngfile_class1_valid": class1_valid,
        "pngfile_class1_test": class1_test
    }

    # 결과를 JSON 파일로 저장
    save_dict_to_json(result_dict, os.path.join(args.dir_pill_class_base, args.json_pill_class_list))

if __name__ == '__main__':
    make_pill_class_list()
