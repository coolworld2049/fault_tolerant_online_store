1. [x] Разработать **упрощенную минималистичную** базу данных интернет-магазина для поддержки каталога с товарами,
   корзин,
   заказов (набор атрибутов на усмотрение студента).
2. [x] Специфицировать операции create/read/update/delete для товаров, корзин, заказов в виде HTTP-запросов (задание
   параметров и методов запросов на усмотрение студента).
    - users crud
3. [x] Материализовать базу данных в PostgreSQL, а веб-сервис на любом языке программирования с применением любых
   средств
    - users crud
4. [x] Настроить мультимастер-репликацию БД с помощью pgpool-II. Количество экземпляров backend не менее двух.
    1. Краткие теоретические сведения из документации
       PostgreSQL: https://www.postgresql.org/docs/current/different-replication-solutions.html
    2. Промежуточное ПО: https://www.pgpool.net/mediawiki/index.php/Main_Page

5. [ ] Продублируйте настроенный экземпляр pgpool-II. Запрограммируйте в веб-приложении круговую смену backend для
   балансировки нагрузки и переподключения в случае сбоя части экземпляров. В качестве backend настраивается не
   экземпляр PostgreSQL, а экземпляр pgpool-II.
6. [ ] Разверните еще один экземпляр веб-сервиса и настройте балансировку нагрузки с помощью nginx.
    1. В случае выбора Tomcat (поддерживаются липкие сессии, ищите на странице sticky
       sessions): https://docs.nginx.com/nginx/deployment-guides/load-balance-third-party/apache-tomcat/
    2. В общем случае: http://nginx.org/en/docs/http/load_balancing.html#nginx_load_balancing_methods
7. [ ] Продублируйте экземпляр nginx.
8. [ ] Подготовьте клиент нагрузочного тестирования например, на python + requests, который будет имитировать поведение
   посетителя-шопоголика. Реализуйте круговую смену backend (nginx). Зафиксируйте среднее время выполнения различных
   запросов из специфицированного в п. 2 API. Сделайте замеры для различного количества экземпляров PostgreSQL,
   pgpool-II, веб-сервиса и nginx. Оцените влияние количества экземпляров компонентов на время выполнения операций
   чтения и записи. Постройте графики среднего времени выполнения каждого запроса для каждой конфигурации. Можно
   оформить в виде нескольких barchart.
9. [ ] Перенесите часть функциональности, например операции над корзиной, в redis. Предположение: модель
   пользователя-шопоголика подразумевает “муки выбора” и частое изменение корзины.
    1. https://github.com/redisson/redisson#Downloads
    2. pip3 install redis
10. [ ] Настройте репликацию в redis. Сделайте доработки, аналогичные п. 5. По умолчанию реплики - read only, можете
    ограничиться балансировкой запросов чтения.
11. [ ] Вновь выполните нагрузочное тестирование и перестройте графики.
12. [ ] Перенесите часть функциональности, например, каталог товаров, в cassandra.
    1. https://cassandra.apache.org/doc/latest/cassandra/getting_started/drivers.html
13. [ ] Настройте кластер cassandra из 3 узлов. Сделайте доработки, аналогичные п. 5. Вы можете поддерживать строгий
    уровень
    согласованности на операциях чтения и записи. https://ru.bmstu.wiki/Apache_Cassandra
14. [ ] Вновь выполните нагрузочное тестирование и перестройте графики.

*Рекомендации к отладочному окружению:* запуск различных экземпляров ПО на разных портах в одной ОС, без контейнеризации
и виртуализации.

*Рекомендации к нагрузочному тестированию:* многомашинные (многоноутбучные) конфигурации с
контейнеризацией/виртуализацией/просто ручным запуском. Клиент нагрузочного тестирования должен быть запущен во
множестве экземпляров. Вам может оказаться полезным:

- На занятиях: витая пара и режимы hot spot wifi-адаптеров в ноутбуках для организации сети (телефоны как роутеры могут
  серьезно ограничить packets per second и не дать собрать статистику).
- Port-Forwarding домой.
- Ресурсы серверной.

Критерии оценки: тройка - графики с PostgreSQL; четверка - графики с PostgreSQL, Redis; пятерка - графики с PostgreSQL,
Redis, Cassandra.