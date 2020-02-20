GET_CAR_PART_DETAILS_BY_CODE = """SELECT cd.id
                            ,cc.code
                            ,cc.name
                            ,cc.display_name
                            ,cc.image
                            ,cd.modelno
                            ,cd.manufacturer
                            ,cd.make
                            ,cd.dimensions
                            ,cd.color
                            ,cd.price
                            ,cd.currency
                            ,cd.manufacturercode
                        FROM carpartcategory cc
                        INNER JOIN carpartdetail cd ON cc.id = cd.category_id
                        WHERE cc.code = '%s'"""

GET_CAR_PART_DETAILS_BY_ID = """SELECT cd.id
                            ,cc.code
                            ,cc.name
                            ,cc.display_name
                            ,cc.image
                            ,cd.modelno
                            ,cd.manufacturer
                            ,cd.make
                            ,cd.dimensions
                            ,cd.color
                            ,cd.price
                            ,cd.currency
                            ,cd.manufacturercode
                        FROM carpartcategory cc
                        INNER JOIN carpartdetail cd ON cc.id = cd.category_id
                        WHERE cd.id = '%s'"""

GET_CAR_PART_CATEGORIES = """SELECT id
                            ,code
                            ,name
                            ,display_name
                        FROM carpartcategory"""

GET_CAR_PART_CATEGORIES_BY_CODE = """SELECT id
                            ,code
                            ,name
                            ,display_name
                            ,image
                        FROM carpartcategory
                        WHERE code = '%s'"""

GET_CAR_PART_CATEGORIES_BY_KEYWORD = """SELECT id
                                        ,code
                                        ,name
                                        ,display_name
                                        ,image
                                        ,(
                                            SELECT COUNT(1)
                                            FROM carpartrelationshiphierarchy
                                            WHERE parent_category_id = cc.id
                                            ) AS [subcategories]
                                        ,(
                                            SELECT COUNT(1)
                                            FROM carpartdetail
                                            WHERE cc.id = category_id
                                            ) AS [variations]
                                    FROM carpartcategory cc
                                    WHERE name LIKE '%%%s%%'"""

GET_CAR_PART_DETAILS_BY_CATEGORIES = """SELECT id
                                        ,code
                                        ,name
                                        ,display_name
                                        ,image
                                        ,(
                                            SELECT COUNT(1)
                                            FROM carpartrelationshiphierarchy
                                            WHERE parent_category_id = cc.id
                                            ) AS [subcategories]
                                        ,(
                                            SELECT COUNT(1)
                                            FROM carpartdetail
                                            WHERE cc.id = category_id
                                            ) AS [variations]
                                    FROM carpartcategory cc
                                    WHERE name IN (%s)"""

GET_CAR_PART_SUB_CATEGORIES_BY_CODE = """SELECT cc2.id
                                            ,cc2.code
                                            ,cc2.name
                                            ,cc2.display_name
                                            ,cc2.image
                                            ,(
                                                SELECT COUNT(1)
                                                FROM carpartrelationshiphierarchy
                                                WHERE parent_category_id = cc2.id
                                                ) AS [subcategories]
                                            ,(
                                                SELECT COUNT(1)
                                                FROM carpartdetail
                                                WHERE cc2.id = category_id
                                                ) AS [variations]
                                        FROM carpartcategory cc1
                                        INNER JOIN carpartrelationshiphierarchy crh ON cc1.id = crh.parent_category_id
                                            AND cc1.code = '%s'
                                        INNER JOIN carpartcategory cc2 ON cc2.id = crh.child_category_id"""

GET_CAR_PART_MAJOR_CATEGORIES = """SELECT cc.id
                                    ,cc.code
                                    ,cc.name
                                    ,cc.display_name
                                    ,cc.image
                                    ,(
                                        SELECT COUNT(1)
                                        FROM carpartrelationshiphierarchy
                                        WHERE parent_category_id = cc.id
                                        ) AS [subcategories]
                                    ,(
                                        SELECT COUNT(1)
                                        FROM carpartdetail
                                        WHERE cc.id = category_id
                                        ) AS [variations]
                                FROM carpartcategory cc
                                INNER JOIN carpartrelationshiphierarchy crh ON cc.id = crh.child_category_id
                                WHERE crh.parent_category_id IS NULL"""

GET_USER_DETAIL_BY_NAME = """SELECT id
                            ,username
                            ,display_name
                            ,email
                            ,expiration_date
                            ,last_active
                        FROM userdetail
                        WHERE username = '{}'
                            AND (expiration_date IS NULL OR strftime('%s', expiration_date) >= strftime('%s', '{}'))"""

GET_USER_PASSWORD = """SELECT password
                        FROM userdetail
                        WHERE username = '{}'"""

UPDATE_LAST_ACTIVE_USER_BY_NAME = """UPDATE userdetail
                                    SET last_active = '{}'
                                    WHERE username = '{}'
                                        AND (expiration_date IS NULL OR strftime('%s', expiration_date) >= strftime('%s', '{}'))"""

GET_CAR_PART_DETAILS_BY_BARCODE = """SELECT id
                                        ,code
                                        ,name
                                        ,display_name
                                        ,image
                                        ,(
                                            SELECT COUNT(1)
                                            FROM carpartrelationshiphierarchy
                                            WHERE parent_category_id = cc.id
                                            ) AS [subcategories]
                                        ,(
                                            SELECT COUNT(1)
                                            FROM carpartdetail
                                            WHERE cc.id = category_id
                                            ) AS [variations]
                                    FROM carpartcategory cc
                                    WHERE code IN (%s)"""
