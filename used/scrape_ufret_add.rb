#coding:utf-8
require 'nokogiri'
require 'anemone'
MAIN_URL="http://www.ufret.jp/song.php?data="
    url=MAIN_URL+"40002"
    key=""
    #簡単弾きkey取得
    Anemone.crawl(url, depth_limit: 0) do |anemone|
        anemone.on_every_page do |page|
            page.doc.xpath("//select[@name='keyselect']/option").each do |node|
                if node.xpath("./text()").to_s=~/簡単弾き/
                    key=node.attr('value')
                end
            end
        end
    end
    #原キー列取得
    Anemone.crawl(url, depth_limit: 0) do |anemone|
        anemone.on_every_page do |page|
            page.doc.xpath("//ruby/rt").each do |node|
                print node.xpath("./text()").to_s+" "
            end
        end
    end
    print key+"\n"
