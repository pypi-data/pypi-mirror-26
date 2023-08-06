# Copyright 2016 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest


class TestEntityAnnotation(unittest.TestCase):
    @staticmethod
    def _get_target_class():
        from google.cloud.vision.entity import EntityAnnotation
        return EntityAnnotation

    def test_logo_annotation(self):
        from tests.unit._fixtures import LOGO_DETECTION_RESPONSE

        entity_class = self._get_target_class()
        logo = entity_class.from_api_repr(
            LOGO_DETECTION_RESPONSE['responses'][0]['logoAnnotations'][0])

        self.assertEqual(logo.mid, '/m/05b5c')
        self.assertEqual(logo.description, 'Brand1')
        self.assertEqual(logo.score, 0.63192177)
        self.assertEqual(logo.bounds.vertices[0].x_coordinate, 78)
        self.assertEqual(logo.bounds.vertices[0].y_coordinate, 162)

    def test_logo_pb_annotation(self):
        from google.cloud.vision_v1.proto import image_annotator_pb2

        description = 'testing 1 2 3'
        locale = 'US'
        mid = 'm/w/45342234'
        score = 0.875
        entity_annotation = image_annotator_pb2.EntityAnnotation()
        entity_annotation.mid = mid
        entity_annotation.locale = locale
        entity_annotation.description = description
        entity_annotation.score = score
        entity_annotation.bounding_poly.vertices.add()
        entity_annotation.bounding_poly.vertices[0].x = 1
        entity_annotation.bounding_poly.vertices[0].y = 2
        entity_annotation.locations.add()
        entity_annotation.locations[0].lat_lng.latitude = 1.0
        entity_annotation.locations[0].lat_lng.longitude = 2.0

        entity_class = self._get_target_class()
        entity = entity_class.from_pb(entity_annotation)

        self.assertEqual(entity.description, description)
        self.assertEqual(entity.mid, mid)
        self.assertEqual(entity.locale, locale)
        self.assertEqual(entity.score, score)
        self.assertEqual(entity.bounds.vertices[0].x_coordinate, 1)
        self.assertEqual(entity.bounds.vertices[0].y_coordinate, 2)
        self.assertEqual(entity.locations[0].latitude, 1.0)
        self.assertEqual(entity.locations[0].longitude, 2.0)
