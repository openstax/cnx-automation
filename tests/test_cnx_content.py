# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.content import Content


@pytest.mark.nondestructive
def test_ncy_not_displayed_amgov(base_url, selenium):
    amgov_uuids = ['c6ee95dd-d10b-430c-8a83-20d5a28334a9', '5fd3ce15-f0ea-47ea-ae8e-84d8f9e2930a',
                   '2979f445-bec9-4ae3-94f9-f9c772ce9e9f', '81163025-bf42-4059-8160-cacca24446dc',
                   '497848cb-d4ad-4b0b-8295-c3dd1c9f7437', '515d833c-0ba2-41ab-96b9-9fbeed85817c',
                   '2e6466e7-f162-4327-82fa-58935ff6991a', '3edaca44-5ab0-4a42-a6b8-4247f6faa221',
                   '9f08b241-bb66-48ed-bfde-aa09adf11145', '621c1d37-0bc1-4190-a1b2-a9331f890b1a',
                   '08dfa8e7-2bd3-44ed-a527-1dfd46b67215', '3dfca04b-06c7-4279-9602-6360152f1f37',
                   'b36f239d-9025-47bf-957e-bbb675d4cd92', '18083da1-5f89-4378-ba19-aa95e6996459',
                   'f6315546-7b9f-4f19-9114-e9e3c4a7f8d9', '9a5be432-ccff-4c68-bd2f-54ee60f1afb2',
                   '55697c4a-b143-4bc6-8831-f75a3c1c06cb', '6e795d7a-5b58-4249-a926-918b62e36454',
                   '81fbf31f-7c89-4a96-9789-48e2b564ad22', 'b7e4fad8-6af8-4a63-a83c-0985ba6ff07b',
                   '6df3591b-d82c-4603-9586-cb7f4fb0af1a', '8a78fac5-9323-4dca-8c28-cd103cce83c8',
                   '8c5fc05a-8a77-4fe5-aabc-fa17072249d5', '49abac0f-b70e-4be9-9cf2-495966413644',
                   'd7f8e6e8-48fb-48d2-9998-e946750e7996', '1db17831-5aba-4aba-aa4a-0146e2e02998',
                   'bda29a31-1f25-4371-8376-785c6a0ddf9a', 'eb93a6f4-edc3-4a02-a26c-59faeae71c4b',
                   '49dc3f4c-22ba-448a-a334-654b7425d867', '6ccea6dd-6e15-437e-a026-4e4ef01c75ad',
                   '7cc1a318-0d76-40e5-ae5a-0a7f52ddf7e2', 'efc2d9ee-e3a6-4ab6-a381-b86ce9075d2d',
                   '7d34ddc8-ed22-4aa0-9e74-b5f5d2a2974b', '7f85b54d-4062-4945-bfa9-2ebca3dd2a61',
                   'ed22cb13-2f14-460f-a603-fb1631f4c6f6', '33651201-eefb-4b44-83d7-692c92be5d85',
                   '27b0fa06-f702-47f9-bc56-776ff4cd74ec', 'bf879400-500f-4feb-8744-452675525e2c',
                   'b622df1d-07e9-4a16-ba51-97993fa74899', '555946f7-b655-4976-b2a7-4c0e6c246330',
                   'f321ca0c-3392-45e1-a76d-092cd31fb2a5', '9c71f4d0-d6df-481b-9996-ce751ca49f96',
                   'f71475e4-c8d2-4a4e-8fca-cf854bb8f31b', 'e9332f2b-7721-463a-9b96-e67c74fc1f5b',
                   '5abe0bea-2667-4c18-bcda-634d14955c44', '2622cf6c-5acf-4b0b-a3f1-9ac89f2ec025',
                   '6681afcf-ddc2-4de4-a4d3-7ee7f94d44ae', 'e99782f8-f975-41a3-a08c-84c907aad93d',
                   '9824235e-9e98-4cf1-af98-f569754dc520', 'a5c1983c-ba62-47b1-877f-a24d8201d5a8',
                   '955cba00-3d51-4fbc-a7b0-0ea8c7b851f9', '0c441e8b-99de-4706-915c-615af32b2aa0',
                   '023c8dc9-73ff-415e-a425-740122f650e4', '1d159c7f-e08c-417d-80aa-8a157a957c76',
                   '9a5cabad-893a-48f7-bce0-339ea4a6e9c0', '76697fff-e01d-4f3e-97c5-eba408cd8009',
                   '851a64e1-b529-4707-951f-b033813b146c', '10c74228-8722-4825-a50f-a9d35b4489d5',
                   '2b8d9fc0-b165-44b0-88de-ad0327cf4c00', '39c1b936-f0dd-4341-a1cb-6c9449f2715f',
                   'fdf44e79-776e-477e-963c-a6c0a98c434a', '76c60115-aa26-4596-b673-a6e12a16c613',
                   'd76b7e9e-cf6a-498f-b9e2-32a57b967577', 'ebd1ac6d-f33e-487e-8906-8d9ad88b9ff1',
                   'a8ae7f1c-0874-499c-b92c-a3690dc92d1c', 'e8568b4f-0c23-44d8-8c56-e0672bc31c8a',
                   '3416922d-f5b2-431d-8793-89ed4b191fbb', 'fa69014a-50c5-4c8d-9b72-d87ee964e83f',
                   '08ada2c8-89d9-4641-b993-bed8515ea23e', '2aafcd29-e648-4b86-b8b7-84d0ce46f906',
                   '4673fb51-9c11-4ffc-b282-a9aeab42d5a0', 'ed844365-afb4-47d1-9428-c4f473e7366e',
                   'a7a5f339-252d-4b50-83ed-a2495bc02779', '8469ef00-4d28-4cd8-99ab-f77b9bbc0acc',
                   '41270e16-46ff-4790-be8a-9c43bfc05254', '75bad956-ba62-4639-92cf-d25fc3bdd9f1',
                   '46814db9-5d28-4e66-a8a4-7c79c484fc45', 'd124704d-7e8a-4c87-bcef-6ce608f3b435',
                   'cb580850-c3f8-4763-914a-442151866495', 'a7afa056-d34b-4390-bf2e-4057701100ca',
                   'f11ccf83-1b1e-4c33-9f37-4ad3e09509e1', '3b22b8ed-450a-4077-b25f-8ee425ad2439',
                   '9f8d0c73-0533-4fe7-9aef-e978b61b27fc']

    for uuid in amgov_uuids:
        ncy_url = 'https://qa.cnx.org/contents/' + uuid
        page = Content(selenium, ncy_url).open()
        assert not page.is_ncy_displayed
