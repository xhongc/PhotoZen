#!/bin/bash

# PhotoZen Docker 构建脚本
# 该脚本帮助构建优化后的 Docker 镜像

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认值
PLATFORM="arm64"
TAG="latest"
BUILD_ENV="prod"
PUSH=false

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -p, --platform PLATFORM    构建平台 (amd64, arm64, both) [默认: amd64]"
    echo "  -t, --tag TAG              镜像标签 [默认: latest]"
    echo "  -e, --env ENVIRONMENT      构建环境 (prod, dev) [默认: prod]"
    echo "  --push                     构建后推送到仓库"
    echo "  -h, --help                 显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 -p amd64 -t v1.0.0"
    echo "  $0 -p both --push"
    echo "  $0 -p arm64 -t latest-arm"
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--platform)
            PLATFORM="$2"
            shift 2
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -e|--env)
            BUILD_ENV="$2"
            shift 2
            ;;
        --push)
            PUSH=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}错误: 未知参数 $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# 验证平台参数
if [[ ! "$PLATFORM" =~ ^(amd64|arm64|both)$ ]]; then
    echo -e "${RED}错误: 平台必须是 amd64, arm64 或 both${NC}"
    exit 1
fi

# 验证环境参数
if [[ ! "$BUILD_ENV" =~ ^(prod|dev)$ ]]; then
    echo -e "${RED}错误: 环境必须是 prod 或 dev${NC}"
    exit 1
fi

# 构建镜像函数
build_image() {
    local arch=$1
    local dockerfile=$2
    local image_tag=$3
    
    echo -e "${GREEN}开始构建 ${arch} 架构镜像...${NC}"
    echo -e "${YELLOW}使用 Dockerfile: ${dockerfile}${NC}"
    echo -e "${YELLOW}镜像标签: ${image_tag}${NC}"
    
    docker build \
        --platform linux/${arch} \
        --build-arg BUILD_ENVIRONMENT=${BUILD_ENV} \
        -f ${dockerfile} \
        -t ${image_tag} \
        .
    
    echo -e "${GREEN}${arch} 架构镜像构建完成${NC}"
    
    # 显示镜像大小
    echo -e "${YELLOW}镜像大小:${NC}"
    docker images ${image_tag} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
}

# 推送镜像函数
push_image() {
    local image_tag=$1
    echo -e "${GREEN}推送镜像: ${image_tag}${NC}"
    docker push ${image_tag}
}

# 主构建逻辑
echo -e "${GREEN}=== PhotoZen Docker 镜像构建 ===${NC}"
echo -e "${YELLOW}平台: ${PLATFORM}${NC}"
echo -e "${YELLOW}标签: ${TAG}${NC}"
echo -e "${YELLOW}环境: ${BUILD_ENV}${NC}"
echo -e "${YELLOW}推送: ${PUSH}${NC}"
echo ""

case $PLATFORM in
    amd64)
        IMAGE_TAG="photozen:${TAG}-amd64"
        build_image "amd64" "compose/django/Dockerfile" "$IMAGE_TAG"
        if [ "$PUSH" = true ]; then
            push_image "$IMAGE_TAG"
        fi
        ;;
    arm64)
        IMAGE_TAG="photozen:${TAG}-arm64"
        build_image "arm64" "compose/django/Dockerfilearm" "$IMAGE_TAG"
        if [ "$PUSH" = true ]; then
            push_image "$IMAGE_TAG"
        fi
        ;;
    both)
        # 构建 AMD64
        AMD64_TAG="photozen:${TAG}-amd64"
        build_image "amd64" "compose/django/Dockerfile" "$AMD64_TAG"
        
        # 构建 ARM64
        ARM64_TAG="photozen:${TAG}-arm64"
        build_image "arm64" "compose/django/Dockerfilearm" "$ARM64_TAG"
        
        # 创建 manifest
        MANIFEST_TAG="photozen:${TAG}"
        echo -e "${GREEN}创建多架构 manifest...${NC}"
        docker manifest create ${MANIFEST_TAG} ${AMD64_TAG} ${ARM64_TAG}
        docker manifest annotate ${MANIFEST_TAG} ${AMD64_TAG} --arch amd64
        docker manifest annotate ${MANIFEST_TAG} ${ARM64_TAG} --arch arm64
        
        if [ "$PUSH" = true ]; then
            push_image "$AMD64_TAG"
            push_image "$ARM64_TAG"
            echo -e "${GREEN}推送 manifest...${NC}"
            docker manifest push ${MANIFEST_TAG}
        fi
        ;;
esac

echo -e "${GREEN}=== 构建完成 ===${NC}"

# 显示所有构建的镜像
echo -e "${YELLOW}构建的镜像列表:${NC}"
docker images | grep photozen | grep ${TAG} 