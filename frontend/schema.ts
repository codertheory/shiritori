/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

/** Type helpers */
type Without<T, U> = { [P in Exclude<keyof T, keyof U>]?: never };
type XOR<T, U> = T | U extends object
  ? (Without<T, U> & U) | (Without<U, T> & T)
  : T | U;
type OneOf<T extends any[]> = T extends [infer Only]
  ? Only
  : T extends [infer A, infer B, ...infer Rest]
  ? OneOf<[XOR<A, B>, ...Rest]>
  : never;

export interface paths {
  "/api/game/": {
    get: operations["api_game_list"];
    post: operations["api_game_create"];
  };
  [key: `/api/game/${string}/join/`]: {
    post: operations["api_game_join_create"];
  };
  [key: `/api/game/${string}/leave/`]: {
    post: operations["api_game_leave_create"];
  };
  [key: `/api/game/${string}/start/`]: {
    post: operations["api_game_start_create"];
  };
  [key: `/api/game/${string}/turn/`]: {
    post: operations["api_game_turn_create"];
  };
  "/api/schema/": {
    /**
     * @description OpenApi3 schema for this API. Format can be selected via content negotiation.
     *
     * - YAML: application/vnd.oai.openapi
     * - JSON: application/vnd.oai.openapi+json
     */
    get: operations["api_schema_retrieve"];
  };
}

export interface components {
  schemas: {
    CreateGame: {
      settings: components["schemas"]["ShiritoriGameSettings"];
    };
    /** @enum {string} */
    LocaleEnum: "en";
    ShiritoriGame: {
      id: string;
      settings: components["schemas"]["ShiritoriGameSettings"];
      player_count: number;
      word_count: number;
      is_finished: boolean;
      winner: components["schemas"]["ShiritoriPlayer"];
      current_player: components["schemas"]["ShiritoriPlayer"];
      turn_time_left: number;
      words: readonly components["schemas"]["ShiritoriGameWord"][];
      players: readonly components["schemas"]["ShiritoriPlayer"][];
      /** Format: date-time */
      created_at: string;
      /** Format: date-time */
      updated_at: string;
      status?: components["schemas"]["StatusEnum"];
      current_turn?: number;
      last_word?: string;
    };
    ShiritoriGameSettings: {
      locale?: components["schemas"]["LocaleEnum"];
      word_length?: number;
      turn_time?: number;
      max_turns?: number;
    };
    ShiritoriGameWord: {
      word?: string;
      /** Format: double */
      score?: number;
      /** Format: double */
      duration?: number;
    };
    ShiritoriPlayer: {
      id: string;
      name: string;
      score: number;
    };
    ShiritoriTurn: {
      word: string;
      duration: number;
    };
    /** @enum {string} */
    StatusEnum: "WAITING" | "PLAYING" | "FINISHED";
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}

export type external = Record<string, never>;

export interface operations {
  api_game_list: {
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ShiritoriGame"][];
        };
      };
    };
  };
  api_game_create: {
    requestBody: {
      content: {
        "application/json": components["schemas"]["CreateGame"];
        "application/x-www-form-urlencoded": components["schemas"]["CreateGame"];
        "multipart/form-data": components["schemas"]["CreateGame"];
      };
    };
    responses: {
      201: {
        content: {
          "application/json": components["schemas"]["ShiritoriGame"];
        };
      };
    };
  };
  api_game_retrieve: {
    parameters: {
      /** @description A unique value identifying this game. */
      path: {
        id: string;
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ShiritoriGame"];
        };
      };
    };
  };
  api_game_join_create: {
    parameters: {
      /** @description A unique value identifying this game. */
      path: {
        id: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["ShiritoriPlayer"];
        "application/x-www-form-urlencoded": components["schemas"]["ShiritoriPlayer"];
        "multipart/form-data": components["schemas"]["ShiritoriPlayer"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ShiritoriPlayer"];
        };
      };
    };
  };
  api_game_leave_create: {
    parameters: {
      /** @description A unique value identifying this game. */
      path: {
        id: string;
      };
    };
    requestBody?: {
      content: {
        "application/json": components["schemas"]["ShiritoriGame"];
        "application/x-www-form-urlencoded": components["schemas"]["ShiritoriGame"];
        "multipart/form-data": components["schemas"]["ShiritoriGame"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ShiritoriGame"];
        };
      };
    };
  };
  api_game_start_create: {
    parameters: {
      /** @description A unique value identifying this game. */
      path: {
        id: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["ShiritoriTurn"];
        "application/x-www-form-urlencoded": components["schemas"]["ShiritoriTurn"];
        "multipart/form-data": components["schemas"]["ShiritoriTurn"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ShiritoriTurn"];
        };
      };
    };
  };
  api_game_turn_create: {
    parameters: {
      /** @description A unique value identifying this game. */
      path: {
        id: string;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["ShiritoriTurn"];
        "application/x-www-form-urlencoded": components["schemas"]["ShiritoriTurn"];
        "multipart/form-data": components["schemas"]["ShiritoriTurn"];
      };
    };
    responses: {
      200: {
        content: {
          "application/json": components["schemas"]["ShiritoriTurn"];
        };
      };
    };
  };
  api_schema_retrieve: {
    /**
     * @description OpenApi3 schema for this API. Format can be selected via content negotiation.
     *
     * - YAML: application/vnd.oai.openapi
     * - JSON: application/vnd.oai.openapi+json
     */
    parameters?: {
      query?: {
        format?: "json" | "yaml";
        lang?:
          | "af"
          | "ar"
          | "ar-dz"
          | "ast"
          | "az"
          | "be"
          | "bg"
          | "bn"
          | "br"
          | "bs"
          | "ca"
          | "cs"
          | "cy"
          | "da"
          | "de"
          | "dsb"
          | "el"
          | "en"
          | "en-au"
          | "en-gb"
          | "eo"
          | "es"
          | "es-ar"
          | "es-co"
          | "es-mx"
          | "es-ni"
          | "es-ve"
          | "et"
          | "eu"
          | "fa"
          | "fi"
          | "fr"
          | "fy"
          | "ga"
          | "gd"
          | "gl"
          | "he"
          | "hi"
          | "hr"
          | "hsb"
          | "hu"
          | "hy"
          | "ia"
          | "id"
          | "ig"
          | "io"
          | "is"
          | "it"
          | "ja"
          | "ka"
          | "kab"
          | "kk"
          | "km"
          | "kn"
          | "ko"
          | "ky"
          | "lb"
          | "lt"
          | "lv"
          | "mk"
          | "ml"
          | "mn"
          | "mr"
          | "ms"
          | "my"
          | "nb"
          | "ne"
          | "nl"
          | "nn"
          | "os"
          | "pa"
          | "pl"
          | "pt"
          | "pt-br"
          | "ro"
          | "ru"
          | "sk"
          | "sl"
          | "sq"
          | "sr"
          | "sr-latn"
          | "sv"
          | "sw"
          | "ta"
          | "te"
          | "tg"
          | "th"
          | "tk"
          | "tr"
          | "tt"
          | "udm"
          | "uk"
          | "ur"
          | "uz"
          | "vi"
          | "zh-hans"
          | "zh-hant";
      };
    };
    responses: {
      200: {
        content: {
          "application/vnd.oai.openapi": {
            [key: string]: Record<string, never> | undefined;
          };
          "application/yaml": {
            [key: string]: Record<string, never> | undefined;
          };
          "application/vnd.oai.openapi+json": {
            [key: string]: Record<string, never> | undefined;
          };
          "application/json": {
            [key: string]: Record<string, never> | undefined;
          };
        };
      };
    };
  };
}
