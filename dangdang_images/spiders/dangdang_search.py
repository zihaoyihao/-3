import os
import scrapy
from dangdang_images.items import DangdangImagesItem

class DangdangSearchSpider(scrapy.Spider):
    name = 'dangdang_search'
    allowed_domains = ['search.dangdang.com','ddimg.cn']
    start_urls = ['https://search.dangdang.com/?key=%CA%E9%B0%FC&act=input']  # 替换为实际的搜索URL
    max_images = 128  # 最大图片下载数量
    max_pages = 28    # 最大页数
    image_count = 0   # 已下载图片数量计数
    page_count = 0    # 已访问页面计数

    def parse(self, response):
        # 检查是否达到爬取的页数限制
        if self.page_count >= self.max_pages or self.image_count >= self.max_images:
            return

        # 获取所有书籍封面图片的 URL
        image_urls = self.extract_image_urls(response)

        for url in image_urls:
            if self.image_count < self.max_images:
                self.image_count += 1
                item = DangdangImagesItem()
                # 使用 response.urljoin 补全 URL
                item['image_urls'] = [response.urljoin(url)]
                print("Image URL:", item['image_urls'])
                yield item
            else:
                return  # 如果图片数量达到限制，停止爬取

        # 控制页面数量并爬取下一页
        self.page_count += 1
        next_page = response.css("li.next a::attr(href)").get()
        if next_page and self.page_count < self.max_pages:
            yield response.follow(next_page, self.parse)

    def extract_image_urls(self, response):
        # 获取所有书籍封面图片的 URL
        image_urls = response.css("img::attr(data-original)").getall()
        if not image_urls:
            # 有些图片URL属性可能是 `src`，尝试备用选择器
            image_urls = response.css("img::attr(src)").getall()
        return image_urls

    import os
    import scrapy
    from dangdang_images.items import DangdangImagesItem
    import concurrent.futures

    class DangdangSearchSpider(scrapy.Spider):
        name = 'dangdang_search'
        allowed_domains = ['search.dangdang.com', 'ddimg.cn']
        start_urls = ['https://search.dangdang.com/?key=%CA%E9%B0%FC&act=input']  # 替换为实际的搜索URL
        max_images = 135  # 最大图片下载数量
        max_pages = 35  # 最大页数
        image_count = 0  # 已下载图片数量计数
        page_count = 0  # 已访问页面计数

        def parse(self, response):
            # 检查是否达到爬取的页数限制
            if self.page_count >= self.max_pages or self.image_count >= self.max_images:
                return

            # 获取所有书籍封面图片的 URL
            image_urls = response.css("img::attr(data-original)").getall()
            if not image_urls:
                # 有些图片URL属性可能是 `src`，尝试备用选择器
                image_urls = response.css("img::attr(src)").getall()

            # 使用 ThreadPoolExecutor 下载图片
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                for url in image_urls:
                    if self.image_count < self.max_images:
                        self.image_count += 1
                        item = DangdangImagesItem()
                        # 使用 response.urljoin 补全 URL
                        item['image_urls'] = [response.urljoin(url)]
                        print("Image URL:", item['image_urls'])
                        futures.append(executor.submit(self.download_image, item))
                    else:
                        break  # 如果图片数量达到限制，停止爬取

            # 控制页面数量并爬取下一页
            self.page_count += 1
            next_page = response.css("li.next a::attr(href)").get()
            if next_page and self.page_count < self.max_pages:
                yield response.follow(next_page, self.parse)

        def download_image(self, item):
            # 获取图片 URL
            image_url = item['image_urls'][0]

            # 确定保存路径
            image_name = image_url.split("/")[-1]  # 从 URL 中提取图片文件名
            save_path = os.path.join('./images2', image_name)

            try:
                # 发送 GET 请求下载图片
                response = requests.get(image_url, stream=True)
                response.raise_for_status()  # 检查请求是否成功

                # 创建目录（如果不存在）
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                # 保存图片到本地
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                self.logger.info(f"Image downloaded and saved to {save_path}")

            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to download image from {image_url}: {e}")