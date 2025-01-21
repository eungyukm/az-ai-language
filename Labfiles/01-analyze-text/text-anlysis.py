from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    try:
        # .env 파일 로드 (필요시 사용)
        load_dotenv()

        # 엔드포인트와 키 설정
        endpoint = "https://az-lg.cognitiveservices.azure.com/"
        key = "SmIxKZ3SYHuHHUvX7FBfY51CW63qo9gsI2Evh7p2v0VwCKYZOYjRJQQJ99BAACNns7RXJ3w3AAAaACOGbV1j"

        # Azure AI 클라이언트 생성
        credential = AzureKeyCredential(key)
        ai_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

        # 'reviews' 폴더 설정 (현재 스크립트 기준 절대 경로)
        reviews_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reviews')

        # 'reviews' 폴더가 존재하는지 확인
        if not os.path.exists(reviews_folder):
            raise FileNotFoundError(f"The 'reviews' folder does not exist at: {reviews_folder}")

        # 폴더 내 모든 파일 처리
        for file_name in os.listdir(reviews_folder):
            file_path = os.path.join(reviews_folder, file_name)

            # 파일인지 확인
            if os.path.isfile(file_path):
                try:
                    # 파일 읽기
                    with open(file_path, encoding='utf8') as file:
                        text = file.read()

                    print(f"\n-------------\nFile: {file_name}")
                    print(f"\nText Content:\n{text}")

                    # Azure Text Analytics API 호출
                    # 언어 감지
                    detected_language = ai_client.detect_language(documents=[text])[0]
                    print(f"\nLanguage: {detected_language.primary_language.name}")

                    # 감정 분석
                    sentiment_analysis = ai_client.analyze_sentiment(documents=[text])[0]
                    print(f"Sentiment: {sentiment_analysis.sentiment}")

                    # 주요 키워드 추출
                    key_phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
                    if key_phrases:
                        print("\nKey Phrases:")
                        for phrase in key_phrases:
                            print(f"  - {phrase}")

                    # 엔티티 추출
                    entities = ai_client.recognize_entities(documents=[text])[0].entities
                    if entities:
                        print("\nEntities:")
                        for entity in entities:
                            print(f"  - {entity.text} ({entity.category})")

                    # 연결된 엔티티 추출
                    linked_entities = ai_client.recognize_linked_entities(documents=[text])[0].entities
                    if linked_entities:
                        print("\nLinked Entities:")
                        for linked_entity in linked_entities:
                            print(f"  - {linked_entity.name} ({linked_entity.url})")

                except Exception as e:
                    print(f"Error processing file {file_name}: {e}")

    except Exception as ex:
        print(f"An error occurred: {ex}")


if __name__ == "__main__":
    main()
